from datetime import datetime

def generate_order_number(db):
    today_str = datetime.now().strftime('%Y%m%d')
    prefix = f"CAN{today_str}"
    
    latest_order = db.orders.find_one(
        {"order_number": {"$regex": f"^{prefix}"}},
        sort=[("order_number", -1)]
    )
    
    if latest_order:
        last_num = int(latest_order['order_number'][-4:])
        new_num = last_num + 1
    else:
        new_num = 1
        
    return f"{prefix}{str(new_num).zfill(4)}"
