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
from services.destino_origen_service import DestinoOrigenService
import json

avion_service = AvionService()
asiento_service = AsientoService()
vuelo_service = VueloService()
destino_origen_service = DestinoOrigenService()

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

@ns.route("", methods=["post", "get"])
class Vuelo(Resource):
    @api.expect(new_vuelo)
    def post(self):
        try:
            payload = request.json
            payload["fecha_salida"]+=":00"
            payload["fecha_llegada"]+=":00"
            vuelo = vuelo_service.add_vuelo(payload)
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
        
    def get(self):
        try:
            response = vuelo_service.get_vuelo()
            if(response):
                result = []
                for vuelo in response:
                    result.append({
                        "id":vuelo.id,
                        "id_avion":vuelo.id_avion,
                        "clave_vuelo":vuelo.clave_vuelo,
                        "origen":vuelo.origen,
                        "destino":vuelo.destino,
                        "fecha_salida":datetime.strftime(vuelo.fecha_salida, "%Y-%m-%d %H:%M:%S"),
                        "fecha_llegada":datetime.strftime(vuelo.fecha_llegada, "%Y-%m-%d %H:%M:%S"),
                        "costo_base":vuelo.costo_base,
                        "created":datetime.strftime(vuelo.created, "%Y-%m-%d %H:%M:%S")
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
        
@ns.route("/<origen>/<destino>/<fecha_salida>/<fecha_llegada>", methods=["get"])
class GetVuelo(Resource):
    def get(self, origen, destino, fecha_salida, fecha_llegada):
        try:
            print(origen)
            response = vuelo_service.get_vuelo_by_origen_destino(origen, destino, fecha_salida, fecha_llegada)
            if(response):
                result = []
                for vuelo in response:
                    result.append({
                        "id":vuelo.id,
                        "id_avion":vuelo.id_avion,
                        "clave_vuelo":vuelo.clave_vuelo,
                        "origen":vuelo.origen,
                        "destino":vuelo.destino,
                        "fecha_salida":datetime.strftime(vuelo.fecha_salida, "%Y-%m-%d %H:%M:%S"),
                        "fecha_llegada":datetime.strftime(vuelo.fecha_llegada, "%Y-%m-%d %H:%M:%S"),
                        "costo_base":vuelo.costo_base,
                        "created":datetime.strftime(vuelo.created, "%Y-%m-%d %H:%M:%S")
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

@ns.route("/<modelo>", methods=["delete"])
class DelVueloModelo(Resource):
    def delete(self, modelo):
        try:
            vuelo = vuelo_service.get_vuelo_by_clave(modelo).id
            response = vuelo_service.del_vuelo_by_id(vuelo)
            if(response):
                return{
                    "id":modelo,
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
        
@ns.route("/origenes_destinos", methods=["get"])
class OrigenDestino(Resource):
    def get(self):
        try:
            response = destino_origen_service.get_origen_destino()
            if(response):
                result = []
                for destino in response:
                    result.append({
                        "values":destino.clave_destino,
                        "label":destino.destino,
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
            
@ns.route("/crear/<clave>/<destino>", methods=["post"])
class PostVueloDestino(Resource):
    def post(self, clave, destino):
        try:
            response = destino_origen_service.add_origen_destino(clave, destino)
            return response, 200
        except Exception as e:
            print(e)
            return{
                "message":"Bad Request"
            },400
        
@ns.route("/destino/<clave>", methods=["delete"])
class DelDestinoClave(Resource):
    def delete(self, clave):
        try:
            response = destino_origen_service.del_destino_by_clave(clave)
            if(response):
                return{
                    "id":clave,
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