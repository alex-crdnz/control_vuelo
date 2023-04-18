import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.vuelo_service import VueloService
from datetime import datetime
from services.asiento_service import AsientoService
from services.avion_service import AvionService
import json

avion_service = AvionService()
asiento_service = AsientoService()
vuelo_service = VueloService()
ns = api.namespace('vuelo', description='Operaciones para obtener datos de los vuelos')

new_vuelo = api.model("new_vuelo",{
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
    @api.expect(new_vuelo)
    def post(self):
        try:
            payload = request.json
            payload["fecha_salida"]+=":00"
            payload["fecha_llegada"]+=":00"
            return(payload)
            vuelo = vuelo_service.add_vuelo(payload)
            if("message" in vuelo):
                conf_asiento = avion_service.get_avion_by_id(vuelo["id_avion"]).configuracion_asientos
                asiento_service.add_asiento_vuelo(json.loads(conf_asiento), vuelo["vuelo_id"])
            else:
                return {
                "body":vuelo
            },400
            return {
                "body":vuelo
            },200
        except Exception as e:
            return {
                "body":"Bad Request"
            },400
        
@ns.route("<clave_vuelo>", methods=["get",])
class GetVuelo(Resource):
    def get(self, clave_vuelo):
        try:
            response = vuelo_service.get_vuelo_by_clave(clave_vuelo)
            if(response):
                return{
                    "body":{
                        "id":response.id,
                        "id_avion":response.id_avion,
                        "clave_vuelo":clave_vuelo,
                        "origen":response.origen,
                        "destino":response.destino,
                        "fecha_salida":datetime.strftime(response.fecha_salida, "%Y-%m-%d %H:%M:%S"),
                        "fecha_llegada":datetime.strftime(response.fecha_llegada, "%Y-%m-%d %H:%M:%S"),
                        "costo_base":response.costo_base,
                        "created":datetime.strftime(response.created, "%Y-%m-%d %H:%M:%S")
                    }
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
