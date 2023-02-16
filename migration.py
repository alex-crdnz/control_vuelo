import db

# import all models
from models.user import User
from models.asiento import Asiento
from models.reservacion import Reservacion
from models.vuelo import Vuelo

def run():
    pass

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    run()