from flask import Blueprint, render_template, request, current_app, redirect, url_for
from models.user import User
from database import db
from flask_login import login_required, logout_user, current_user, login_user
import bcrypt
from app import login_manager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username') 
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            current_app.logger.debug('Created user {} with email {} and password {}'.format(username, email, password))
            login_user(new_user)
            return redirect(url_for('index.index'))    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user is None or not user.check_password(request.form.get('password')):
            current_app.logger.debug('Wrong username or password.')
        else:
            current_app.logger.debug('Found user {} with password {}'.format(user, request.form.get('password')))
            login_user(user)
            return redirect(url_for('index.index')) 
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
