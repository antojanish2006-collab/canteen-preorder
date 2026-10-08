# College Canteen Pre-Order System

## Description
Campus Canteen is a complete, functional College Canteen Pre-Order System built as a Web Frameworks micro project. It allows college students to securely order food ahead of time, pay on pickup, and avoid waiting in long queues. The admin can manage food items and track daily orders seamlessly.

## Features
**Student Features:**
- Register and login securely using hashing
- Browse dynamic food menus
- Search and filter by category
- Add items to cart and manipulate quantities
- Select pickup times and place an order
- View order status via visual tracker
- View complete order histories

**Admin Features:**
- Secure Admin login and dashboard access
- Create, Read, Update, Delete (CRUD) menu items
- Toggle food availability 
- Control order statuses (Pending -> Confirmed -> Preparing -> Ready for Pickup -> Completed)
- View dynamic dashboard statistics and revenue reporting

## Technology Stack
- **Python / Flask**: Backend Web Framework
- **MongoDB / PyMongo**: NoSQL Database for robust data modeling
- **HTML / CSS / JavaScript**: Frontend & Vanilla styling
- **Jinja2**: Template engine
- **Werkzeug**: Password hashing for security

## Installation

### 1. Requirements
- Python 3.8+
- Local MongoDB installed OR MongoDB Atlas Cluster

### 2. Setup (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a file named `.env` in the root (you can copy `.env.example`):
```text
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=canteen_db
SECRET_KEY=CanteenPreorderSuperSecretKey
```
*Note: If using MongoDB Atlas, replace the URI with your Atlas string.*

### 4. Seed Database
Populate the database with sample admin, students, and menu items:
```powershell
python seed.py
```

### 5. Run Application
```powershell
python app.py
```
The application should now be accessible at `http://127.0.0.1:5000`

## MongoDB Setup
### Local MongoDB
1. Ensure MongoDB Community Server is installed and running on port 27017.
2. Ensure your `.env` contains: `MONGO_URI=mongodb://localhost:27017/`

### MongoDB Atlas
1. Create a free cluster on MongoDB Atlas.
2. Obtain the connection string.
3. Replace the `.env` URI with your Atlas connection string, e.g.:
`MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority`
