import sys
sys.path.append("..")

from context import db
from db import Base

class Asiento(Base):
    __tablename__ = 'asiento'
    id = db.Column(db.Integer, primary_key=True)
    id_vuelo = db.Column(db.Integer, db.ForeignKey('vuelo.id'), nullable=False)
    clave_reservacion = db.Column(db.Integer, db.ForeignKey('reservacion.id'), nullable=True)
    clave_asiento = db.Column(db.String(30), nullable=False)
    ventana = db.Column(db.String(30), nullable=False)
    pasillo = db.Column(db.String(30), nullable=False)
    clase = db.Column(db.String(30), nullable=False)
    disponible = db.Column(db.Integer, nullable=True)
    costo_base = db.Column(db.String(30), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    



    def __init__(self, id_vuelo, clave_reservacion, clave_asiento, ventana, pasillo, clase, disponible, costo_base, created):
        self.id_vuelo = id_vuelo,
        self.clave_reservacion = clave_reservacion,
        self.clave_asiento = clave_asiento,
        self.ventana = ventana,
        self.pasillo = pasillo,
        self.clase = clase,
        self.disponible = disponible,
        self.costo_base = costo_base,
        self.created = created
