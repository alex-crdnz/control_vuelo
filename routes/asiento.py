import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request

ns = api.namespace('asiento', description='Operaciones para obtener datos de los asientos')

@ns.route("/", methods=["post"])
class Asiento(Resource):
    def post(self):
        data = request.json