import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request

ns = api.namespace('user', description='Operaciones para obtener datos de los usuarios')

@ns.route("/", methods=["post"])
class User(Resource):
    def post(self):
        data = request.json