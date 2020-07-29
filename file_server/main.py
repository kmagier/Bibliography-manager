from flask import Flask
from flask import (Flask, request, render_template, redirect, url_for,
    send_file, make_response, session, flash)
import os, sys
from database import db
import psycopg2 
from config import *
from flask_login import LoginManager
app = Flask(__name__, static_url_path = "")  
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()  
db.app = app 

from models.article import Article
from models.user import User
from routes.files import files_bp
db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(files_bp)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return "Unauthorized request"