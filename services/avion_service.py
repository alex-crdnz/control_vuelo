import sys
sys.path.append("..")
from context import db
from models.avion import Avion
from models.vuelo import Vuelo
from models.asiento import Asiento
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
    
    def get_configuracion_asiento(self, payload):
        filas_letras = ["A", "B", "C", "D", "E", "F"]
        filas_num = [1, 1, 1, 1, 1, 1]
        filas_cont = 0
        conf_asiento = []
        vip = payload["vip"].split(",")
        premium = payload["premium"].split(",")
        costoVip = payload["costoVip"]
        costoPremium = payload["costoPremium"]
        costoStandard = payload["costoStandard"]
        for _ in range (int(payload["filas"])):
            letra = filas_letras[filas_cont]
            numero = filas_num[filas_cont]
            clave_asiento = letra+str(numero)
            pasillo = None
            ventana = None
            clase = None
            costo_base = None
            if(letra == "A" or letra=="F"):
                ventana = True
                pasillo = False
            if(letra == "B" or letra=="E"):
                ventana = False
                pasillo = False
            if(letra == "C" or letra=="D"):
                ventana = False
                pasillo = True
            if(str(numero) in vip):
                clase = "VIP"
                costo_base = costoVip
            elif(str(numero) in premium):
                clase = "PREMIUM"
                costo_base = costoPremium
            else:
                clase = "STANDARD"
                costo_base = costoStandard
            
            conf_asiento.append({
                "clave_asiento": clave_asiento,
                "ventana": ventana,
                "pasillo": pasillo,
                "clase": clase,
                "costo_base": costo_base
            })
            filas_num[filas_cont]+=1
            filas_cont+=1
            if filas_cont == len(filas_letras):
                filas_cont=0
        return conf_asiento
    
    def get_avion_by_clave(self, clave_avion):
        """consulta la tabla avion por id

        Args:
            vuelo (string): clave_vuelo del vuelo

        Returns:
            Object: Avion
        """            
        try:
            result = Avion.query.filter_by(modelo=clave_avion).first()
        except Exception as e:
            print("mysql error(avion_service/get_avion_by_clave()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def del_avion_by_id(self, id):
        """consulta la tabla avion por id

        Args:
            vuelo (string): clave_vuelo del vuelo

        Returns:
            Object: Avion
        """            
        try:
            self.del_vuelo_by_id_avion(id)
            result = Avion.query.filter_by(id=id).first()
            db.session.delete(result)
            db.session.commit()
        except Exception as e:
            print("mysql error(avion_service/del_avion_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def del_vuelo_by_id_avion(self, id_avion):
        """consulta la tabla asiento por vuelo_id

        Args:
            vuelo (int): id del vuelo

        Returns:
            Object: Asiento
        """            
        try:
            result = Vuelo.query.filter_by(id_avion=id_avion).all()
            for vuelo in result:
                self.del_asiento_by_id(vuelo.id)
                db.session.delete(vuelo)
                db.session.commit()
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