import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request

ns = api.namespace('vuelo', description='Operaciones para obtener datos de los vuelos')

@ns.route("/", methods=["post"])
class Vuelo(Resource):
    def post(self):
        data = request.json