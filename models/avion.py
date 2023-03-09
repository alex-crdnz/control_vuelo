import sys
sys.path.append("..")

from context import db
from db import Base

class Avion(db.Model):
    __tablename__ = 'avion'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(30), nullable=False)
    configuracion_asientos = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


    def __init__(self, modelo, status, configuracion_asientos, created):
        self.modelo = modelo,
        self.status = status,
        self.configuracion_asientos = configuracion_asientos,
        self.created = created
