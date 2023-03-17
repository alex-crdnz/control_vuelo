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
            result = User.query.filterby(email=email, password=password).first()
        except Exception as e:
            print("mysql error(user_service/get_login()): "+str(e))
            db.session.rollback()
        return True if result is not None else False