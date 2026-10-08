import os
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'canteen_db')

def seed_database():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    if not db.users.find_one({'email': 'admin@canteen.com'}):
        db.users.insert_one({
            'name': 'Administrator',
            'register_number': 'ADMIN001',
            'email': 'admin@canteen.com',
            'password_hash': generate_password_hash('admin123'),
            'role': 'admin'
        })
        print("Created admin user.")
    else:
        print("Admin user already exists.")
        
    student_emails = ['student1@college.com', 'student2@college.com']
    for i, email_addr in enumerate(student_emails, 1):
        if not db.users.find_one({'email': email_addr}):
            db.users.insert_one({
                'name': f'Student {i}',
                'register_number': f'23IT{str(i).zfill(3)}',
                'email': email_addr,
                'password_hash': generate_password_hash('student123'),
                'role': 'student'
            })
            print(f"Created student user {i}.")
        else:
             print(f"Student user {i} already exists.")
             
    menu_items = [
        {"name": "Masala Dosa", "description": "Crispy dosa served with chutney and sambar", "category": "Breakfast", "price": 45, "image": "https://images.unsplash.com/photo-1627448398863-71d533ec1b68?w=500&q=80", "is_available": True},
        {"name": "Idli", "description": "Soft idlis served with chutney and sambar", "category": "Breakfast", "price": 30, "image": "https://images.unsplash.com/photo-1626082927389-6cd097cb6acb?w=500&q=80", "is_available": True},
        {"name": "Poori", "description": "Hot pooris with potato masala", "category": "Breakfast", "price": 35, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80", "is_available": True},
        {"name": "Pongal", "description": "Traditional ghee pongal", "category": "Breakfast", "price": 35, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80", "is_available": True},
        {"name": "Veg Meals", "description": "Full vegetarian meals with rice and curries", "category": "Lunch", "price": 60, "image": "https://plus.unsplash.com/premium_photo-1678129321447-bc97e5df0016?w=500&q=80", "is_available": True},
        {"name": "Fried Rice", "description": "Vegetable fried rice", "category": "Lunch", "price": 50, "image": "https://images.unsplash.com/photo-1603133872878-684f67c3f3fa?w=500&q=80", "is_available": True},
        {"name": "Samosa", "description": "Crispy potato stuffed samosa", "category": "Snacks", "price": 10, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80", "is_available": True},
        {"name": "Sandwich", "description": "Grilled vegetable sandwich", "category": "Snacks", "price": 40, "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500&q=80", "is_available": True},
        {"name": "Tea", "description": "Hot Indian tea", "category": "Beverages", "price": 10, "image": "https://images.unsplash.com/photo-1576092762791-dd9e2220abd4?w=500&q=80", "is_available": True},
        {"name": "Coffee", "description": "Filter coffee", "category": "Beverages", "price": 15, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500&q=80", "is_available": True}
    ]
    
    if db.menu_items.count_documents({}) == 0:
        db.menu_items.insert_many(menu_items)
        print(f"Created {len(menu_items)} menu items.")
    else:
        print("Menu items already exist.")

if __name__ == '__main__':
    seed_database()
