import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request

ns = api.namespace('avion', description='Operaciones para obtener datos de los aviones')

@ns.route("/", methods=["post"])
class Avion(Resource):
    def post(self):
        data = request.json