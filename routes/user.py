import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.user_service import UserService
from datetime import datetime
import json

ns = api.namespace('user', description='Operaciones para obtener datos de los usuarios')
user_service = UserService()

user_field = api.model("user_field",{
    "email":fields.String(example="correo@gmail.com"),
    "password":fields.Boolean(example="*********"),
    "name":fields.Boolean(example="Nombre Basico"),
    "last_name":fields.String(example="Apellido Basico")
})

@ns.route("", methods=["post"])
class User(Resource):
    @api.expect(user_field)
    def post(self):
        try:
            return {
                "body":user_service.add_user(request.json)
            },200
        except Exception as e:
            return {
                "body":"Bad Request"
            },400
        
@ns.route("<id>", methods=["get",])
class GetUser(Resource):
    def get(self, id):
        try:
            response = user_service.get_user_by_id(id)
            if(response):
                return{
                    "body":{
                        "id":response.id,
                        "email":response.email,
                        "password":response.password,
                        "name":response.name,
                        "last_name":response.last_name,
                        "status":"activo" if response.status == 1 else "inactivo" ,
                        "created":datetime.strftime(response.created, "%Y-%m-%d %H:%M:%S")
                    }
                }, 200
            else:
                return{
                    "body":"Not Found"
                },404
        except Exception as e:
            return{
                "body":"Bad Request"
            },400