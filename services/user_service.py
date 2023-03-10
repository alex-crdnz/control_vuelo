import sys
sys.path.append("..")
from context import db
from models.user import User
from datetime import datetime
import json

class UserService:
    def add_user(self, payload):
        """Agrega user a la tabla avion

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id del user
        """        
        try:
            if all(key in payload for key in ("email","password","name","last_name")):
                if (self.get_user_by_email(payload["email"])):
                    return f"Ya existe el email {payload['email']}"
                result = User(
                    email=payload["email"],
                    password=payload["password"],
                    name=payload["name"],
                    last_name=payload["last_name"],
                    status=1,
                    created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
        except Exception as e:
            print("mysql error(user_service/add_user()): "+str(e))
            db.session.rollback()
            return {"message":"Ha ocurrido un error al crear el user"}
        return {
            "message":"user creado correctamente",
            "user_id":result.id,
        }

    def get_user_by_id(self, id):
        """consulta la tabla user por id

        Args:
            id (string): id del id_user

        Returns:
            Object: Avion
        """            
        try:
            result = User.query.filter_by(id=id).first()
        except Exception as e:
            print("mysql error(user_service/get_user_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False
    
    def get_user_by_email(self, email):
        """consulta la tabla user por id

        Args:
            id (string): id del id_user

        Returns:
            Object: Avion
        """            
        try:
            result = User.query.filter_by(email=email).first()
        except Exception as e:
            print("mysql error(user_service/get_user_by_email()): "+str(e))
            db.session.rollback()
        return result if result is not None else False