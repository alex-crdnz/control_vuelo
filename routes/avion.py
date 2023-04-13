import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.avion_service import AvionService
from datetime import datetime
import json

avion_service = AvionService()
ns = api.namespace('avion', description='Operaciones para obtener datos de los aviones')

asientos_field_configuracion = api.model("asientos_field_configuracion",{
    "clave_asiento":fields.String(example="A1"),
    "ventana":fields.Boolean(example=True),
    "pasillo":fields.Boolean(example=False),
    "clase":fields.String(example="VIP"),
    "costo_base":fields.String(example="999")
})

configuracion_field_asientos = api.model("configuracion_field_asientos",{
    "asientos":fields.List(fields.Nested(asientos_field_configuracion))
})

avion_field = api.model("avion_field",{
    "modelo":fields.String(example="AV_GDFS1287"),
    "configuracion_asientos":fields.Nested(configuracion_field_asientos),
})

@ns.route("", methods=["post", "get"])
class Avion(Resource):
    @api.expect(avion_field)
    def post(self):
        try:
            return avion_service.add_avion(request.json), 200
        except Exception as e:
            return {
                "message":"Bad Request"
            },400
    
    def get(self):
        try:
            response = avion_service.get_avion()
            if(response):
                result = []
                for vuelo in response:
                    result.append({
                        "id":vuelo.id,
                        "modelo":vuelo.modelo,
                    })
                return result, 200
            else:
                return{
                    "message":"Not Found"
                },404
        except Exception as e:
            print(e)
            return{
                "message":"Bad Request"
            },400
        
@ns.route("<id>", methods=["get",])
class GetAvion(Resource):
    def get(self, id):
        try:
            response = avion_service.get_avion_by_id(id)
            if(response):
                return{
                    "id":response.id,
                    "modelo":response.modelo,
                    "configuracion_asientos":json.loads(response.configuracion_asientos),
                    "created":datetime.strftime(response.created, "%Y-%m-%d %H:%M:%S")
                }, 200
            else:
                return{
                    "body":"Not Found"
                },404
        except Exception as e:
            return{
                "body":"Bad Request"
            },400
