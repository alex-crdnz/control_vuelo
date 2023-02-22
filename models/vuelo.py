import sys
sys.path.append("..")

from context import db
from db import Base

class Vuelo(db.Model):
    __tablename__ = 'vuelo'
    id = db.Column(db.Integer, primary_key=True)
    id_avion = db.Column(db.Integer, db.ForeignKey('avion.id'), nullable=False)
    clave_vuelo = db.Column(db.String(10), nullable=False)
    origen = db.Column(db.String(30), nullable=False)
    destino = db.Column(db.String(30), nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    fecha_llegada = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, id_avion, clave_vuelo, origen, destino, fecha_salida, fecha_llegada, created):
        self.clave_vuelo = clave_vuelo,
        self.id_avion = id_avion,
        self.origen = origen,
        self.destino = destino,
        self.fecha_salida = fecha_salida,
        self.fecha_llegada = fecha_llegada,
        self.created = created
