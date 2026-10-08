from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.mongo import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        from database.mongo import db
        if db is None:
            flash('Database connection failed. Cannot authenticate.', 'error')
            return render_template('login.html')
            
        user = db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            session['name'] = user['name']
            session['register_number'] = user.get('register_number', '')
            
            flash('Login successful', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid credentials', 'error')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        register_number = request.form.get('register_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([full_name, register_number, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('Passwords must match', 'error')
            return redirect(url_for('auth.register'))
            
        if len(password) < 6:
            flash('Password minimum 6 characters', 'error')
            return redirect(url_for('auth.register'))
            
        from database.mongo import db
        if db is None:
            flash('Database connection failed. Cannot register.', 'error')
            return redirect(url_for('auth.register'))
            
        # Check unique constraints
        if db.users.find_one({'email': email}):
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
            
        if db.users.find_one({'register_number': register_number}):
            flash('Register number already registered', 'error')
            return redirect(url_for('auth.register'))
            
        user_doc = {
            'name': full_name,
            'register_number': register_number,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': 'student',
            'created_at': datetime.now()
        }
        
        db.users.insert_one(user_doc)
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
