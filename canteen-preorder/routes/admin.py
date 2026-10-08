from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.decorators import admin_required
from bson.objectid import ObjectId
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@admin_required
def check_admin():
    pass

@admin_bp.route('/dashboard')
def dashboard():
    from database.mongo import db
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    
    # Aggregation for better performance (as requested)
    status_counts = list(db.orders.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))
    
    counts = {stat['_id']: stat['count'] for stat in status_counts}
    
    total_orders = sum(counts.values())
    pending_orders = counts.get('Pending', 0)
    preparing_orders = counts.get('Preparing', 0)
    ready_orders = counts.get('Ready for Pickup', 0)
    completed_orders = counts.get('Completed', 0)
    
    total_items = db.menu_items.count_documents({})
    available_items = db.menu_items.count_documents({'is_available': True})
    
    # Today's revenue via aggregation
    revenue_agg = list(db.orders.aggregate([
        {"$match": {"created_at": {"$gte": today_start}, "status": {"$ne": "Cancelled"}}},
        {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
    ]))
    today_revenue = revenue_agg[0]['total'] if revenue_agg else 0
    
    return render_template('admin/dashboard.html',
                          total_orders=total_orders,
                          pending_orders=pending_orders,
                          preparing_orders=preparing_orders,
                          ready_orders=ready_orders,
                          completed_orders=completed_orders,
                          total_items=total_items,
                          available_items=available_items,
                          today_revenue=today_revenue)

@admin_bp.route('/menu')
def menu():
    from database.mongo import db
    items = list(db.menu_items.find())
    return render_template('admin/menu.html', items=items)

@admin_bp.route('/menu/add', methods=['GET', 'POST'])
def add_item():
    from database.mongo import db
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        image = request.form.get('image')
        is_available = 'is_available' in request.form
        
        if not name or not category or price <= 0:
            flash('Invalid input', 'error')
            return redirect(url_for('admin.add_item'))
            
        item_doc = {
            'name': name,
            'description': description,
            'category': category,
            'price': price,
            'image': image or '/static/images/default.jpg',
            'is_available': is_available,
            'created_at': datetime.now()
        }
        
        db.menu_items.insert_one(item_doc)
        flash('Menu item added', 'success')
        return redirect(url_for('admin.menu'))
        
    return render_template('admin/add_item.html')

@admin_bp.route('/menu/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    from database.mongo import db
    item = db.menu_items.find_one({'_id': ObjectId(item_id)})
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        image = request.form.get('image')
        is_available = 'is_available' in request.form
        
        db.menu_items.update_one({'_id': ObjectId(item_id)}, {'$set': {
            'name': name,
            'description': description,
            'category': category,
            'price': price,
            'image': image,
            'is_available': is_available
        }})
        
        flash('Menu item updated', 'success')
        return redirect(url_for('admin.menu'))
        
    return render_template('admin/edit_item.html', item=item)

@admin_bp.route('/menu/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    from database.mongo import db
    db.menu_items.delete_one({'_id': ObjectId(item_id)})
    flash('Menu item deleted', 'success')
    return redirect(url_for('admin.menu'))

@admin_bp.route('/menu/toggle/<item_id>', methods=['POST'])
def toggle_item(item_id):
    from database.mongo import db
    item = db.menu_items.find_one({'_id': ObjectId(item_id)})
    if item:
        db.menu_items.update_one({'_id': ObjectId(item_id)}, {'$set': {'is_available': not item['is_available']}})
        flash('Item availability updated', 'success')
    return redirect(url_for('admin.menu'))

@admin_bp.route('/orders')
def orders():
    from database.mongo import db
    all_orders = list(db.orders.find().sort('created_at', -1))
    return render_template('admin/orders.html', orders=all_orders)

@admin_bp.route('/orders/<order_number>', methods=['GET', 'POST'])
def order_detail(order_number):
    from database.mongo import db
    order = db.orders.find_one({'order_number': order_number})
    if not order:
        abort(404)
        
    if request.method == 'POST':
        new_status = request.form.get('status')
        # Implement logical status transitions check if strictly required, or just trust admin dropdown
        db.orders.update_one({'order_number': order_number}, {'$set': {'status': new_status}})
        flash('Order status updated', 'success')
        return redirect(url_for('admin.order_detail', order_number=order_number))
        
    return render_template('admin/order_detail.html', order=order)
