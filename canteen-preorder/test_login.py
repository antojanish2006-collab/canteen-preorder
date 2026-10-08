import requests

session = requests.Session()
login_data = {'email': 'admin@canteen.com', 'password': 'admin123'}
resp = session.post('http://127.0.0.1:5000/login', data=login_data)
if resp.status_code == 200:
    print("Login successful")

orders_resp = session.get('http://127.0.0.1:5000/admin/orders')
print("Orders access status:", orders_resp.status_code)
# Extract an order number from HTML 
import re
match = re.search(r'order_number=([A-Z0-9]+)', orders_resp.text)
if match:
    order_number = match.group(1)
    print("Found order:", order_number)
    
    # Test valid order 
    detail_resp = session.get(f'http://127.0.0.1:5000/admin/orders/{order_number}') 
    print(f"Order detail code: {detail_resp.status_code}")
    if "Ordered Items" in detail_resp.text:
       print("Renders items")
    if "built-in" in detail_resp.text or "TypeError" in detail_resp.text:
       print("ERROR still present")
else:
    print("No orders generated yet, placing a dummy order")
    # Need student login to place order
    session2 = requests.Session()
    session2.post('http://127.0.0.1:5000/login', data={'email': 'student1@college.com', 'password': 'student123'})
    
    # get a menu item
    menu = session2.get('http://127.0.0.1:5000/student/menu')
    # Let me just stop and see if there are any orders.
