import os
from pymongo import MongoClient

client = None
db = None

def init_db(app):
    global client
    global db
    mongo_uri = app.config.get('MONGO_URI')
    database_name = app.config.get('DATABASE_NAME')
    
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        
        # Create indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("register_number", unique=True)
        db.orders.create_index("order_number", unique=True)
        db.orders.create_index("user_id")
        db.menu_items.create_index("category")
        db.menu_items.create_index("is_available")
        
    except Exception as e:
        client = None
        db = None
        print(f"Failed to connect to MongoDB: {e}")
