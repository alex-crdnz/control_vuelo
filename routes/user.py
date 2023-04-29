import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.user_service import UserService
from datetime import datetime
import json

user_service = UserService()
ns = api.namespace('user', description='Operaciones para obtener datos de los usuarios')

user_field_datos = api.model("user_field_datos",{
    "email":fields.String(example="newuser@hotmail.com"),
    "password":fields.String(example="Contra$sena5"),
    "name":fields.String(example="Nuevo"),
    "last_name":fields.String(example="Usuario"),
    "status":fields.String(example="1")
})

login_user = api.model("login_user",{
    "email":fields.String(example="example@hotmail.com"),
    "password":fields.String(example="ExamplePassword")
})

@ns.route("", methods=["post"])
class User(Resource):
    @api.expect(user_field_datos)
    def post(self):
        try:
            return user_service.add_user(request.json), 200
        except Exception as e:
            return {
                "message":"Bad Request"
            },400

@ns.route("/login", methods=["post"])
class Login(Resource):
    @api.expect(login_user)
    def post(self):
        try:
            data = request.json
            response = user_service.get_login(data["email"], data["password"])
            if(response):
                return{ 
                    "message":"Credenciales correctas",
                    "role":response.role   
                    }, 200
            else:
                return{
                    "body":"Not Found"
                },404
        except Exception as e:
            print(e)
            return{
                "body":"Bad Request"
            },400