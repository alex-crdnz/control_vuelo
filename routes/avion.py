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

form_avion_field = api.model("form_avion_field",{
    "modelo":fields.String(example="AV_GFRD34"),
    "filas":fields.Boolean(example="60"),
    "vip":fields.Boolean(example="1,2,3"),
    "costoVip":fields.String(example="900"),
    "premium":fields.String(example="8,9,10"),
    "costoPremium":fields.String(example="700"),
    "costoStandard":fields.String(example="500")
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
                    vip=0
                    cv=0
                    standard=0
                    cs=0
                    premium=0
                    cp=0
                    for asiento in json.loads(vuelo.configuracion_asientos)["asientos"]:
                        if (asiento["clase"].lower() == "vip"):
                            vip+=1
                            cv=asiento["costo_base"]
                        if (asiento["clase"].lower() == "standard"):
                            standard+=1
                            cs=asiento["costo_base"]
                        if (asiento["clase"].lower() == "premium"):
                            cp=asiento["costo_base"]
                            premium+=1    
                    result.append({
                        "id":vuelo.id,
                        "modelo":vuelo.modelo,
                        "asientos_standard":standard,
                        "costo_base_standard":cs,
                        "asientos_vip":vip,
                        "costo_base_vip":cv,
                        "asientos_premium":premium,
                        "costo_base_premium":cp
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
        
@ns.route("/<modelo>", methods=["delete",])
class DeleteAvion(Resource):
    def delete(self, modelo):
        try:
            avion = avion_service.get_avion_by_clave(modelo).id
            response = avion_service.del_avion_by_id(avion)
            if(response):
                return{
                    "id":modelo,
                    "message":"avion eliminado correctamente"
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
        
@ns.route("/form", methods=["post"])
class AvionAsientos(Resource):
    @api.expect(form_avion_field)
    def post(self):
        data =request.json
        try:
            if all(key in data for key in ("modelo","filas","vip","costoVip",
            "premium", "costoPremium", "costoStandard")):
                payload = {
                    "modelo": data["modelo"],
                    "configuracion_asientos": {
                        "asientos": avion_service.get_configuracion_asiento(data)
                    }
                }
                return avion_service.add_avion(payload), 200
        except Exception as e:
            print(e)
            return {
                "message":"Bad Request"
            },400