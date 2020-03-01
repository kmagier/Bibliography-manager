from datetime import datetime
from models.user import User
from database import db

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), index=True, unique=True)
    title = db.Column(db.String(200), index=True, unique=True)
    pages = db.Column(db.Integer, index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_path = db.Column(db.String(256), index=True, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Article id: {}>'.format(self.id)
