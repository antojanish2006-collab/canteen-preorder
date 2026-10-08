from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.decorators import login_required
from utils.helpers import generate_order_number
from datetime import datetime
from bson.objectid import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.before_request
@login_required
def check_student():
    if session.get('role') != 'student':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('admin.dashboard'))

@student_bp.route('/dashboard')
def dashboard():
    from database.mongo import db
    user_id = session['user_id']
    
    total_orders = db.orders.count_documents({'user_id': ObjectId(user_id)})
    completed_orders = db.orders.count_documents({'user_id': ObjectId(user_id), 'status': 'Completed'})
    
    active_order = db.orders.find_one(
        {'user_id': ObjectId(user_id), 'status': {'$nin': ['Completed', 'Cancelled']}},
        sort=[('created_at', -1)]
    )
    
    return render_template('student/dashboard.html', 
                          total_orders=total_orders,
                          completed_orders=completed_orders,
                          active_order=active_order)

@student_bp.route('/menu')
def menu():
    from database.mongo import db
    category = request.args.get('category', 'All')
    search = request.args.get('search', '')
    
    query = {}
    if category != 'All':
        query['category'] = category
    if search:
        query['name'] = {'$regex': search, '$options': 'i'}
        
    items = list(db.menu_items.find(query))
    return render_template('student/menu.html', items=items, current_category=category, current_search=search)

@student_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    from database.mongo import db
    if 'cart' not in session:
        session['cart'] = {}
        
    if request.method == 'POST':
        action = request.form.get('action')
        item_id = request.form.get('item_id')
        
        if action == 'add':
            item = db.menu_items.find_one({'_id': ObjectId(item_id)})
            if item and item.get('is_available'):
                # Add item to cart
                cart = session.get('cart', {})
                cart[item_id] = cart.get(item_id, 0) + 1
                session['cart'] = cart
                session.modified = True
                flash('Item added to cart', 'success')
            else:
                flash('Item is unavailable', 'error')
        
        elif action == 'update':
            quantity = int(request.form.get('quantity', 0))
            cart = session.get('cart', {})
            if quantity > 0:
                cart[item_id] = quantity
            else:
                cart.pop(item_id, None)
            session['cart'] = cart
            session.modified = True
            
        elif action == 'remove':
            cart = session.get('cart', {})
            cart.pop(item_id, None)
            session['cart'] = cart
            session.modified = True
            flash('Item removed', 'success')
            
        if request.form.get('redirect') == 'menu':
            return redirect(url_for('student.menu'))
        return redirect(url_for('student.cart'))

    cart_items = []
    total = 0
    for item_id, quantity in session['cart'].items():
        item = db.menu_items.find_one({'_id': ObjectId(item_id)})
        if item:
            subtotal = item['price'] * quantity
            total += subtotal
            item['quantity'] = quantity
            item['subtotal'] = subtotal
            cart_items.append(item)
            
    return render_template('student/cart.html', cart_items=cart_items, total=total)

@student_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    from database.mongo import db
    if not session.get('cart'):
        flash('Cart is empty', 'error')
        return redirect(url_for('student.menu'))
        
    cart_items = []
    total = 0
    
    for item_id, quantity in session['cart'].items():
        item = db.menu_items.find_one({'_id': ObjectId(item_id)})
        if not item or not item.get('is_available'):
            flash(f'Item is no longer available.', 'error')
            return redirect(url_for('student.cart'))
            
        subtotal = item['price'] * quantity
        total += subtotal
        cart_items.append({
            'menu_item_id': item['_id'],
            'name': item['name'],
            'quantity': quantity,
            'price': item['price'],
            'subtotal': subtotal
        })
        
    if request.method == 'POST':
        pickup_time = request.form.get('pickup_time')
        
        order_doc = {
            'order_number': generate_order_number(db),
            'user_id': ObjectId(session['user_id']),
            'student_name': session['name'],
            'register_number': session['register_number'],
            'items': cart_items,
            'total_amount': total,
            'pickup_time': pickup_time,
            'payment_method': 'Cash on Pickup',
            'payment_status': 'Pending',
            'status': 'Pending',
            'created_at': datetime.now()
        }
        
        db.orders.insert_one(order_doc)
        session.pop('cart', None)
        flash('Order placed successfully', 'success')
        return redirect(url_for('student.order_success', order_number=order_doc['order_number']))
        
    return render_template('student/checkout.html', cart_items=cart_items, total=total)

@student_bp.route('/order-success/<order_number>')
def order_success(order_number):
    from database.mongo import db
    order = db.orders.find_one({'order_number': order_number, 'user_id': ObjectId(session['user_id'])})
    if not order:
        return redirect(url_for('student.dashboard'))
    return render_template('student/order_success.html', order=order)

@student_bp.route('/orders')
def orders():
    from database.mongo import db
    user_orders = list(db.orders.find({'user_id': ObjectId(session['user_id'])}).sort('created_at', -1))
    return render_template('student/orders.html', orders=user_orders)

@student_bp.route('/orders/<order_number>')
def order_detail(order_number):
    from database.mongo import db
    order = db.orders.find_one({'order_number': order_number, 'user_id': ObjectId(session['user_id'])})
    if not order:
        abort(404)
    return render_template('student/order_detail.html', order=order)
