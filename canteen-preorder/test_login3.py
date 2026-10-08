import requests

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
