from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from datetime import datetime
import requests
import re

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DATABASE_NAME')]

# Get admin and student
student = db.users.find_one({'email': 'student1@college.com'})
menu_item = db.menu_items.find_one()

# Create dummy order
order = {
    'order_number': 'CAN202610080001',
    'user_id': student['_id'],
    'student_name': student['name'],
    'register_number': student['register_number'],
    'items': [{
        'menu_item_id': menu_item['_id'],
        'name': menu_item['name'],
        'quantity': 2,
        'price': menu_item['price'],
        'subtotal': menu_item['price'] * 2
    }],
    'total_amount': menu_item['price'] * 2,
    'pickup_time': '12:30 PM',
    'payment_method': 'Cash on Pickup',
    'payment_status': 'Pending',
    'status': 'Pending',
    'created_at': datetime.now()
}
db.orders.insert_one(order)
print("Dummy order inserted!")

# TEST VIA HTTP
session = requests.Session()
session.post('http://127.0.0.1:5000/login', data={'email': 'admin@canteen.com', 'password': 'admin123'})
detail_resp = session.get('http://127.0.0.1:5000/admin/orders/CAN202610080001')

print(f"Order detail code: {detail_resp.status_code}")
if "Ordered Items" in detail_resp.text:
    print("SUCCESS: Renders items")
if "TypeError" in detail_resp.text:
    print("FAILURE: Error still present")
if detail_resp.status_code == 200:
    print("Page loads perfectly!")
else:
    print(detail_resp.text)
    
# TEST 404
invalid_resp = session.get('http://127.0.0.1:5000/admin/orders/CAN_INVALID_123')
print(f"Invalid order status code: {invalid_resp.status_code}")
