import sys
sys.path.append("..")
from context import db
from models.reservacion import Reservacion
from models.user import User
from datetime import datetime
# from services.user_service import UserService
from services.asiento_service import AsientoService
from services.vuelo_service import VueloService
import json

class ReservacionService:
    def add_reservacion(self, payload):
        """Agrega vuelo a la tabla reservacion

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id de la reservacion
        """        
        if all(key in payload for key in ("id_user","clave_reservacion","status","costo_total",
            "configuracion")):
            try:
                if (self.get_reservacion_by_clave(payload["clave_reservacion"])):
                    return f"Ya existe la clave_reservacion {payload['clave_reservacion']}"
                # user_id = UserService.get_user_by_id(self, payload["id_user"])
                # if (user_id) == False:
                #     return f"El user con id {payload['id_user']} no existe"
                asientos = []
                vuelos = []
                for vuelo in (payload["configuracion"]["vuelo"]):
                    vuelo_id = VueloService.get_vuelo_by_clave(self, vuelo["clave_vuelo"])
                    if(vuelo_id == False):
                        return {"message":"Ha ocurrido un error con la seleccion de vuelo"}
                    asiento = AsientoService.get_asiento(self, vuelo_id.id, vuelo["clave_asiento"], 1)
                    if(asiento == False):
                        return {"message":"Ha ocurrido un error con la seleccion de asientos"}
                    asientos.append(asiento.clave_asiento)
                    vuelos.append(vuelo_id.id)
                for update in range(len(asientos)):
                    AsientoService.update_siento(self, vuelos[update],asientos[update], 1)
                result = Reservacion(
                    id_user=int(payload["id_user"]),
                    clave_reservacion=payload["clave_reservacion"],
                    status=payload["status"],
                    costo_total=payload["costo_total"],
                    configuracion=json.dumps({"configuracion":payload["configuracion"]}),
                    created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
            except Exception as e:
                print("mysql error(reservacion_service/add_reservacion()): "+str(e))
                db.session.rollback()
                return {"message":"Ha ocurrido un error al crear la reservacion"}
        return {
            "message":"reservacion creada correctamente",
            "reservacion_id":result.id,
            "clave_reservacion":result.clave_reservacion[0]
        }
    
    def get_reservacion_by_clave(self, clave_reservacion):
        """consulta la tabla reservacion por clave

        Args:
            vuelo (string): clave_reservacion de la reservacion

        Returns:
            Object: reservacion
        """            
        try:
            result = Reservacion.query.filter_by(clave_reservacion=clave_reservacion).first()
        except Exception as e:
            print("mysql error(reservacion_service/get_reservacion_by_clave()): "+str(e))
            db.session.rollback()
        return result if result is not None else False