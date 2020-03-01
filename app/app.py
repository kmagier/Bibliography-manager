from flask import Flask
from flask import (Flask, request, render_template, redirect, url_for,
    send_file, make_response, session, flash)
import redis
import os, sys
from database import db
import psycopg2
from config import *
from views.index.index import index_bp
from views.auth.auth import auth_bp


app = Flask(__name__, static_url_path = "")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
db.app = app

from models.user import User
from models.article import Article
db.init_app(app)
db.create_all()
# db.init_app(app) 
# db.create_all(app)

app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)

  