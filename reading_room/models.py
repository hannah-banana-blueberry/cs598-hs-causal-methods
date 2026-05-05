from sqlalchemy import MetaData, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Excerpt(db.Model):
    __tablename__ = 'excerpts'
    id = db.Column(db.Integer, primary_key=True)
    excerpt_title = db.Column(db.Text, nullable=False)
    excerpt_author = db.Column(db.Text, nullable=False)
    excerpt_number = db.Column(db.Integer, nullable=False)
    excerpt_condition = db.Column(db.String(50))
    excerpt_json = db.Column(db.Text, nullable=False)


    # Used in __init__.py to grab question
    def from_db(self):
        return {
            'id': self.id,
            'excerpt_title': self.excerpt_title,
            'excerpt_author': self.excerpt_author,
            'excerpt_number': self.excerpt_number,
            'excerpt_json' : json.loads(self.excerpt_json)
        }
    
    def __repr__(self):
        return f"The excerpt author is {self.excerpt_author}."

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    date_completed = db.Column(db.DateTime, default=datetime.now)

    # Relationship(s)
    attempts = db.relationship('Attempt', back_populates='user_attempt')

    def __repr__(self):
        return f"User's username is {self.username}."


class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(20), db.ForeignKey('users.username'))
    excerpt_title = db.Column(db.Text)
    excerpt_author = db.Column(db.Text)
    excerpt_number = db.Column(db.Integer)
    attempt_number = db.Column(db.Integer)
    date_completed = db.Column(db.DateTime, default=datetime.now)

    # Relationship(s)
    user_attempt = db.relationship('User', back_populates='attempts')
    
    def __repr__(self):
        return f"The user completed excerpt #{self.excerpt_number}."
    