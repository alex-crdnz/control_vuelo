import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.vuelo_service import VueloService
from datetime import datetime
from services.asiento_service import AsientoService
import json

asiento_service = AsientoService()
vuelo_service = VueloService()
ns = api.namespace('asiento', description='Operaciones para obtener datos de los asientos')

@ns.route("<clave_vuelo>", methods=["get",])
class GetUser(Resource):
    def get(self, clave_vuelo):
        try:
            vuelo = vuelo_service.get_vuelo_by_clave(clave_vuelo)
            if vuelo== False:
                return{
                    "body":"Not Found"
                },404
            asientos = asiento_service.get_asiento_by_id(vuelo.id)
            response = {
                "asientos":[]
            }
            for asiento in asientos:
                response["asientos"].append(
                    {
                        "id":str(asiento.id),
                        "clave_vuelo":str(clave_vuelo),
                        "clave_reservacion":str(asiento.clave_reservacion),
                        "clave_asiento":str(asiento.clave_asiento),
                        "ventana":"si" if asiento.ventana == "1" else "no",
                        "pasillo":"si" if asiento.pasillo == "1" else "no",
                        "clase":str(asiento.clase),
                        "disponible":"disponible" if asiento.disponible == 1 else "no disponible",
                        "costo_base":str(asiento.costo_base),
                        "created":str(asiento.created)
                    }
                )
            return{
                "body":response
            }, 200
        except Exception as e:
            return{
                "body":"Bad Request"
            },400