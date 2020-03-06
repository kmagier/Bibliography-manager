from flask import Flask
from flask import (Flask, request, render_template, redirect, url_for,
    send_file, make_response, session, flash)
import redis
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

from views.index.index import index_bp 
from views.auth.auth import auth_bp
from views.articles.articles import articles_bp
from models.user import User
from models.article import Article 
db.init_app(app)
login_manager.init_app(app)
db.create_all()

app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(articles_bp) 

  