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
                result = Vuelo(
                id_avion=AvionService.get_avion_by_id(self, payload["id_avion"]).id,
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
            "clave_vuelo":result.clave_vuelo[0]
        }