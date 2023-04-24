import sys
sys.path.append("..")
from context import db
from models.aeropuerto import Aeropuerto

class DestinoOrigenService():
    def get_origen_destino(self):
      try:
          result = Aeropuerto.query.filter_by().all()
      except Exception as e:
          print("mysql error(DestinoOrigenService/get_origen_destino()): "+str(e))
          db.session.rollback()
      return result if result is not None else False
    
    def add_origen_destino(self,clave, destino):
      try:
        result = Aeropuerto(
          clave_destino=clave,
          destino=destino
        )
        db.session.add(result)
        db.session.commit()
      except Exception as e:
          print("mysql error(user_service/add_user()): "+str(e))
          db.session.rollback()
          return {"message":"Ha ocurrido un error al crear el nuevo destino."}
      return {
          "id":result.id,
          "message":"nuevo destino creado correctamente"
      }
    
    def del_destino_by_clave(self, clave):
      try:
          result = Aeropuerto.query.filter_by(clave_destino=clave).first()
          db.session.delete(result)
          db.session.commit()
      except Exception as e:
          print("mysql error(vuelo_service/delete_vuelo_by_id()): "+str(e))
          db.session.rollback()
      return result if result is not None else False