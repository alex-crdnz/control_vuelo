import sys
sys.path.append("..")

from context import db
from db import Base

class Aeropuerto(db.Model):
    __tablename__ = 'aeropuerto'
    id = db.Column(db.Integer, primary_key=True)
    clave_destino = db.Column(db.String(30), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    tua = db.Column(db.String(50), nullable=False)

    def __init__(self, clave_destino, destino, tua):
        self.clave_destino = clave_destino,
        self.destino = destino,
        self.tua = tua
