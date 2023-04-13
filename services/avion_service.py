import sys
sys.path.append("..")
from context import db
from models.avion import Avion
from datetime import datetime
import json


class AvionService:
    def add_avion(self, payload):
        """Agrega avion a la tabla avion

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id del avion
        """        
        try:
            if all(key in payload for key in ("modelo","configuracion_asientos")):
                result = Avion(
                    modelo=payload["modelo"],
                    configuracion_asientos=json.dumps(payload["configuracion_asientos"]),
                    created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
        except Exception as e:
            print("mysql error(aavion_service/add_avion()): "+str(e))
            db.session.rollback()
            return {"message":"Ha ocurrido un error al crear el avion"}
        return {
            "id":result.id,
            "message":"avion creado correctamente"
        }

    def get_avion_by_id(self, id):
        """consulta la tabla avion por id

        Args:
            id (string): id del id_avion

        Returns:
            Object: Avion
        """            
        try:
            result = Avion.query.filter_by(id=id).first()
        except Exception as e:
            print("mysql error(avion_service/get_avion_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def get_avion(self):
        """consulta la tabla avion por id

        Args:
            vuelo (string): clave_vuelo del vuelo

        Returns:
            Object: Avion
        """            
        try:
            result = Avion.query.filter_by().all()
        except Exception as e:
            print("mysql error(vuelo_service/get_avion()): "+str(e))
            db.session.rollback()
        return result if result is not None else False