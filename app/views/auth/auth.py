from flask import Blueprint, render_template, request, current_app
from models.user import User
from database import db
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get('username') 
       email = request.form.get('email')
       password = request.form.get('password')
       current_app.logger.debug('Created user {} with email {} and password {}'.format(username, email, password))
       new_user = User(username=username, email=email, password=password)
       db.session.add(new_user)
       db.session.commit()
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first().username == username and User.query.filter_by(username=username).first().password == password:
            current_app.logger.debug('Found user {} with password {}'.format(username, password))
            return render_template('index.html')
        else:
            current_app.logger.debug('Wrong username or password.')
    return render_template('login.html')

# def check_user(username):
#     if User.query.filter_by(username=username).first() == None
#     return {'User doesn\'t exist'}