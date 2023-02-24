import sys
sys.path.append("..")

from context import db
from db import Base

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(70), nullable=False)
    name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, email, password, name, last_name, status, created):
        self.email = email,
        self.password = password,
        self.name = name,
        self.last_name = last_name,
        self.status = status,
        self.created = created
