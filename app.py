from context import app
import routes.user
import routes.vuelos
import routes.asiento
import routes.reservacion

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)