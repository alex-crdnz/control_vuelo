import sys
sys.path.append("..")
from context import db
from models.user import User
from datetime import datetime
import json


class UserService:
    def add_user(self, payload):
        """Agrega un nuevo usuario a la tabla user

        Args:
            payload (dict): diccionario con los datos de las tablas

        Returns:
            dict: diccionaro con el mensaje de la tabla y id de usuario
        """        
        try:
            if all(key in payload for key in ("email","password", "name", "last_name", "status")):
                if (self.get_user_by_email(payload["email"])):
                    return f"Ya existe el email {payload['email']}"
                result = User(
                    email=payload["email"],
                    password=payload["password"],
                    name=payload["name"],
                    last_name=payload["last_name"],
                    status=payload["status"],
                    created= datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(result)
                db.session.commit()
        except Exception as e:
            print("mysql error(user_service/add_user()): "+str(e))
            db.session.rollback()
            return {"message":"Ha ocurrido un error al crear el nuevo usuario."}
        return {
            "id":result.id,
            "message":"nuevo usuario creado correctamente"
        }

    def get_login(self, email, password):
        """consulta la tabla user

        Args:
            email (string): email del id_user
            password (string): contraseña del id_user

        Returns:
            Boolean: True
        """            
        try:
            result = User.query.filter_by(email=email, password=password).first()
        except Exception as e:
            print("mysql error(user_service/get_login()): "+str(e))
            db.session.rollback()
        return True if result is not None else False
    
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