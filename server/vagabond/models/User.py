from vagabond.__main__ import db
from bcrypt import hashpw, gensalt

class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    actors = db.relationship('Actor')


    def __init__(self, username, password, display_name = None):
        self.username = username.lower()
        self.password_hash = hashpw(bytes(password, 'utf-8'), gensalt())
        if display_name != None:
            self.display_name = display_name
