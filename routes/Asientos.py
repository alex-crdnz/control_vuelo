import sys
sys.path.append("..")
from dotenv import load_dotenv
from context import api
from flask_restplus import Resource, fields
from flask import request
from services.asiento_service import AsientoService
from services.vuelo_service import VueloService
from datetime import datetime
import json

asiento_service = AsientoService()
vuelo_service = VueloService()
ns = api.namespace('asiento', description='Operaciones para obtener datos de los usuarios')

@ns.route("/<clave>", methods=["get"])
class Asiento(Resource):
    def get(self, clave):
        try:
            id_vuelo = vuelo_service.get_vuelo_by_clave(clave).id
            response = asiento_service.get_asiento_by_id(id_vuelo)
            if(response):
                result = []
                for asiento in response:
                    result.append({
                        "clave_reservacion":"no reservada" if (asiento.clave_reservacion==None) else asiento.clave_reservacion,
                        "clave_asiento":asiento.clave_asiento,
                        "ventana":"si" if (asiento.ventana=="1") else "no",
                        "pasillo":"si" if (asiento.pasillo=="1") else "no",
                        "clase":asiento.clase,
                        "disponible":"si" if (asiento.disponible==1) else "no",
                        "costo_base":asiento.costo_base
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