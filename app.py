from context import app
import routes.user
import routes.vuelos
import routes.reservacion
import routes.avion
import routes.asiento

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)