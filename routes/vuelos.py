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
            vuelo = vuelo_service.add_vuelo(request.json)
            if("message" in vuelo):
                conf_asiento = avion_service.get_avion_by_id(vuelo["id_avion"]).configuracion_asientos
                asiento_service.add_asiento_vuelo(json.loads(conf_asiento), vuelo["vuelo_id"])
            else:
                return vuelo, 400
            return {
                "id":vuelo["vuelo_id"],
                "message":vuelo["message"]
            }, 200
        except Exception as e:
            return {
                "message":"Bad Request"
            },400
        
@ns.route("<origen><destino>", methods=["get"])
class GetVuelo(Resource):
    def get(self, origen, destino):
        try:
            print(origen)
            response = vuelo_service.get_vuelo_by_origen_destino(origen, origen)
            if(response):
                return{
                    "id":response.id,
                    "id_avion":response.id_avion,
                    "clave_vuelo":response.clave_vuelo,
                    "origen":response.origen,
                    "destino":response.destino,
                    "fecha_salida":datetime.strftime(response.fecha_salida, "%Y-%m-%d %H:%M:%S"),
                    "fecha_llegada":datetime.strftime(response.fecha_llegada, "%Y-%m-%d %H:%M:%S"),
                    "costo_base":response.costo_base,
                    "created":datetime.strftime(response.created, "%Y-%m-%d %H:%M:%S")
                }, 200
            else:
                return{
                    "message":"Not Found"
                },404
        except Exception as e:
            print(e)
            return{
                "message":"Bad Request"
            },400

@ns.route("<id>", methods=["delete",])
class DelVuelo(Resource):
    def delete(self, id):
        try:
            response = vuelo_service.del_vuelo_by_id(id)
            if(response):
                return{
                    "id":id,
                    "message":"vuelo eliminado correctamente"
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