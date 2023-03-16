import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from datetime import datetime
import json

ns = api.namespace('reservacion', description='Operaciones para obtener datos de las reservaciones')

@ns.route("", methods=["post"])
class Reservacion(Resource):
    def post(self):
        return 0
    