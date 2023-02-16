import sys
sys.path.append("..")

from context import db
from db import Base

class Asiento(db.Model):
    __tablename__ = 'asiento'
    id = db.Column(db.Integer, primary_key=True)
    id_vuelo = db.Column(db.Integer, db.ForeignKey('vuelo.id'), nullable=False)
    clave_asiento = db.Column(db.String(30), nullable=False)
    clase = db.Column(db.String(30), nullable=False)
    equipaje = db.Column(db.String(30), nullable=True)
    costo = db.Column(db.String(70), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    



    def __init__(self, id_vuelo, clave_asiento, clase, equipaje, costo, status, created):
        self.id_vuelo = id_vuelo,
        self.clave_asiento = clave_asiento,
        self.clase = clase,
        self.equipaje = equipaje,
        self.costo = costo,
        self.status = status,
        self.created = created
