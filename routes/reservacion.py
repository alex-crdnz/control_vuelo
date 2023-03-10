import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from services.reservacion_service import ReservacionService
from flask import request
from datetime import datetime
import json

ns = api.namespace('reservacion', description='Operaciones para obtener datos de las reservaciones')
reservacion_service = ReservacionService()

documentado_mano_field = api.model("documentado_mano_field",{
    "peso":fields.String(example="10")
})

equipaje_field = api.model("equipaje_field",{
    "documentado/mano":fields.Nested(documentado_mano_field)
})

vuelo_field = api.model("vuelo_field",{
    "clave_vuelo":fields.String(example="V1_VJSV78"),
    "clave_asiento":fields.String(example="A1"),
    "equipaje":fields.List(fields.Nested(equipaje_field))
})

configuracion_field = api.model("configuracion_field",{
    "vuelo":fields.List(fields.Nested(vuelo_field))
})

reservacion_field = api.model("reservacion_field",{
    "id_user":fields.Integer(example=1),
    "clave_reservacion":fields.String(example="RS_VJSV78"),
    "status":fields.String(example="Activo"),
    "costo_total":fields.String(example="2500"),
    "configuracion":fields.Nested(configuracion_field),
})

@ns.route("", methods=["post"])
class Reservacion(Resource):
    @api.expect(reservacion_field)
    def post(self):
        try:
            return {
                "body":reservacion_service.add_reservacion(request.json)
            },200
        except Exception as e:
            return {
                "body":e
            },400
        
@ns.route("<clave_reservacion>", methods=["get",])
class GetReservacion(Resource):
    def get(self, clave_reservacion):
        try:
            response = reservacion_service.get_reservacion_by_clave(clave_reservacion)
            if(response):
                return{
                    "body":{
                        "id":response.id,
                        "id_user":response.id_user,
                        "clave_reservacion":clave_reservacion,
                        "status":response.status,
                        "costo_total":response.costo_total,
                        "configuracion":json.loads(response.configuracion),
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
