import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.vuelo_service import VueloService

vuelo_service = VueloService()
ns = api.namespace('vuelo', description='Operaciones para obtener datos de los vuelos')

vuelo_field = api.model("vuelo_field",{
    "id_avion":fields.Integer(example=1),
    "clave_vuelo":fields.String(example="V1_VJSV78"),
    "origen":fields.String(example="Mexico"),
    "destino":fields.String(example="Florida"),
    "fecha_salida":fields.String(example="YYYY-MM-DD 00:00:00"),
    "fecha_llegada":fields.String(example="YYYY-MM-DD 00:00:00"),
    "costo_base":fields.String(example="999.99")
})

@ns.route("", methods=["post"])
class Vuelo(Resource):
    @api.expect(vuelo_field)
    def post(self):
        try:
            return {
                "body":vuelo_service.add_vuelo(request.json)
            },200
        except Exception as e:
            return {
                "body":e
            },400