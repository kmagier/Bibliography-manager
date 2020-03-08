from database import db
import bcrypt
from flask_sqlalchemy import inspect
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(256), index=True, unique=True)
    articles = db.relationship('Article', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
