import sys
sys.path.append("..")

from context import db
from db import Base

class Reservacion(db.Model):
    __tablename__ = 'reservacion'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_asiento = db.Column(db.Integer, db.ForeignKey('asiento.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, id_user, id_asiento, status, created):
        self.id_user = id_user,
        self.id_asiento = id_asiento,
        self.status = status,
        self.created = created
