import sys
sys.path.append("..")
from context import db
from models.asiento import Asiento
from models.reservacion import Reservacion
from datetime import datetime
from services.avion_service import AvionService
import json
from sqlalchemy.types import Boolean

class AsientoService:
    def add_asiento_vuelo(self, asientos, id_vuelo):
        """Agrega asiento a la tabla asiento

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id del asiento
        """        
        try:
            for asiento in asientos["asientos"]:
                result = Asiento(
                    id_vuelo=id_vuelo,
                    clave_reservacion=None,
                    clave_asiento=asiento["clave_asiento"],
                    ventana=asiento["ventana"],
                    pasillo=asiento["pasillo"],
                    clase=asiento["clase"],
                    costo_base=asiento["costo_base"],
                    disponible=1,
                    created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
        except Exception as e:
            print("mysql error(asiento_service/add_asiento()): "+str(e))
            db.session.rollback()
            return {"message":"Ha ocurrido un error al crear la reservacion"}
        return {
            "message":"asientos creados correctamente"
        }
    
    def get_siento(self, id_vuelo, clave_asiento, disponible):
        """consulta la tabla reservacion por clave

        Args:
            vuelo (string): clave_reservacion de la reservacion

        Returns:
            Object: reservacion
        """            
        try:
            result = Asiento.query.filter_by(id_vuelo=id_vuelo, clave_asiento=clave_asiento, disponible=disponible).first()
        except Exception as e:
            print("mysql error(asiento_service/get_siento()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def update_siento(self, id_vuelo, clave_asiento, disponible):
        """consulta la tabla reservacion por clave

        Args:
            vuelo (string): clave_reservacion de la reservacion

        Returns:
            Object: reservacion
        """            
        try:
            result = Asiento.query.filter_by(id_vuelo=id_vuelo, clave_asiento=clave_asiento, disponible=disponible).first()
            result.disponible=0
        except Exception as e:
            print("mysql error(asiento_service/update_siento()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def get_asiento_by_id(self, id_vuelo):
        """consulta la tabla asiento por vuelo_id

        Args:
            vuelo (int): id del vuelo

        Returns:
            Object: Asiento
        """            
        try:
            result = Asiento.query.filter_by(id_vuelo=id_vuelo).all()
        except Exception as e:
            print("mysql error(asiento_service/get_asiento_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def del_asiento_by_id(self, id_vuelo):
        """consulta la tabla asiento por vuelo_id

        Args:
            vuelo (int): id del vuelo

        Returns:
            Object: Asiento
        """            
        try:
            result = Asiento.query.filter_by(id_vuelo=id_vuelo).all()
            for asiento in result:
                db.session.delete(asiento)
                db.session.commit()
        except Exception as e:
            print("mysql error(asiento_service/get_asiento_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False