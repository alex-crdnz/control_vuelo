import sys
sys.path.append("..")
from context import db
from models.vuelo import Vuelo
from datetime import datetime
from services.avion_service import AvionService

class VueloService:
    def add_vuelo(self, payload):
        """Agrega vuelo a la tabla vuelo

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id del vuelo
        """        
        if all(key in payload for key in ("id_avion","clave_vuelo","origen","destino",
            "fecha_salida", "fecha_llegada", "costo_base")):
            try:
                if (self.get_vuelo_by_clave(payload["clave_vuelo"])):
                    return f"Ya existe la clave_vuelo {payload['clave_vuelo']}"
                avion_id = AvionService.get_avion_by_id(self, payload["id_avion"])
                if (avion_id) == False:
                    return f"El avion con id {payload['id_avion']} no existe"
                result = Vuelo(
                id_avion=avion_id.id,
                clave_vuelo=payload["clave_vuelo"],
                origen=payload["origen"],
                destino=payload["destino"],
                fecha_salida=datetime.strptime(payload["fecha_salida"], "%Y-%m-%d %H:%M:%S"),
                fecha_llegada=datetime.strptime(payload["fecha_llegada"], "%Y-%m-%d %H:%M:%S"),
                costo_base=payload["costo_base"],
                created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
            except Exception as e:
                print("mysql error(vuelo_service/add_vuelo()): "+str(e))
                db.session.rollback()
                return {"message":"Ha ocurrido un error al crear el vuelo"}
        return {
            "message":"vuelo creado correctamente",
            "vuelo_id":result.id,
            "clave_vuelo":result.clave_vuelo[0],
            "id_avion":result.id_avion[0]
        }
    
    def get_vuelo_by_clave(self, clave_vuelo):
        """consulta la tabla avion por id

        Args:
            vuelo (string): clave_vuelo del vuelo

        Returns:
            Object: Avion
        """            
        try:
            result = Vuelo.query.filter_by(clave_vuelo=clave_vuelo).first()
        except Exception as e:
            print("mysql error(vuelo_service/get_vuelo_by_clave()): "+str(e))
            db.session.rollback()
        return result if result is not None else False