import sys
sys.path.append("..")

from context import db
from db import Base

class Vuelo(db.Model):
    __tablename__ = 'vuelo'
    id = db.Column(db.Integer, primary_key=True)
    clave_vuelo = db.Column(db.String(10), nullable=False)
    lugar_salida = db.Column(db.String(30), nullable=False)
    lugar_destino = db.Column(db.String(30), nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    fecha_llegada = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, clave_vuelo, lugar_salida, lugar_destino, fecha_salida, fecha_llegada, created):
        self.clave_vuelo = clave_vuelo,
        self.lugar_salida = lugar_salida,
        self.lugar_destino = lugar_destino,
        self.fecha_salida = fecha_salida,
        self.fecha_llegada = fecha_llegada,
        self.created = created
