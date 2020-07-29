from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from models.user import User
from database import db
from flask_login import login_required, logout_user, current_user, login_user
import bcrypt
from app import login_manager
from forms.authForms import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index.index'))    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is None or not user.check_password(request.form.get('password')):
            return redirect(request.url)
        else:
            login_user(user)
            return redirect(url_for('index.index')) 
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = current_user
    form = PasswordChangeForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        current_password = form.password.data
        new_password = form.new_password.data
        if not user.check_password(form.password.data):
            return redirect(request.url)
        else:
            user.set_password(new_password)
            db.session.commit()
            return redirect(url_for('index.index'))
    return render_template('change-password.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
