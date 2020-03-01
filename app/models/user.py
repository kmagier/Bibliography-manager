from database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(256), index=True, unique=True)
    articles = db.relationship('Article', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
