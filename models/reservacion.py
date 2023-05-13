import sys
sys.path.append("..")

from context import db
from db import Base

class Reservacion(db.Model):
    __tablename__ = 'reservacion'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clave_reservacion = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    costo_total = db.Column(db.String(30), nullable=False)
    configuracion = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, id_user, clave_reservacion, status, costo_total, configuracion, created):
        self.id_user = id_user,
        self.clave_reservacion = clave_reservacion,
        self.status = status,
        self.costo_total = costo_total,
        self.configuracion = configuracion,
        self.created = created
