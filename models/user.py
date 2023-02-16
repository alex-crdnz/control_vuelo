import sys
sys.path.append("..")

from context import db
from db import Base

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(70), nullable=False)
    user_key = db.Column(db.String(70), nullable=False)
    name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    telefono = db.Column(db.String(70), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, user, user_key, name, last_name, email, telefono, status, created):
        self.user = user,
        self.user_key = user_key,
        self.name = name,
        self.last_name = last_name,
        self.email = email,
        self.telefono = telefono,
        self.status = status,
        self.created = created
