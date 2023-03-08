import sys
sys.path.append("..")
from context import db
from models.avion import Avion

class AvionService:
    def get_avion_by_id(self, id):
        """consulta la tabla avion por id

        Args:
            id (string): id del id_avion

        Returns:
            Object: Avion
        """            
        try:
            result = Avion.query.filter_by(id=id).first()
        except Exception as e:
            print("mysql error(avion_service/get_avion_by_id()): "+str(e))
            db.session.rollback()
        return result if result is not None else False