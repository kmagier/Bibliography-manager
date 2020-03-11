from flask import url_for
from datetime import datetime
from models.user import User
from database import db
from flask_sqlalchemy import inspect

BASE_URL = 'https://localhost:8081'

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), index=True)
    title = db.Column(db.String(200), index=True)
    pages = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    article_hash = db.Column(db.String(80), index=True, unique=True)
    org_filename = db.Column(db.String(256), index=True)
    file_path = db.Column(db.String(256), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Article id: {}>'.format(self.id)
    
    def serialize(self):
        return {"id": self.id,
                "author": self.author,
                "title": self.title,
                "pages": self.pages,
                "download_link": BASE_URL + url_for('files.download_article', article_name=self.article_hash) if self.file_path is not "" else ""
                        }
