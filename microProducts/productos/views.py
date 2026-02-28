from flask import Flask
from productos.controllers.producto_controller import producto_controller
from db.db import db
from flask_cors import CORS
from flask_consulate import Consul
import os

app = Flask(__name__)
CORS(app)

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "products-service")
SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 5003))
SERVICE_HOST = os.environ.get("SERVICE_HOST", "microproducts")

consul = Consul(app=app, host=CONSUL_HOST)

consul.register_service(
    name=SERVICE_NAME,
    interval='5s',
    tags=['products', 'flask'],
    port=SERVICE_PORT,
    httpcheck=f'http://{SERVICE_HOST}:{SERVICE_PORT}/healthcheck',
    address=SERVICE_HOST
)

# Configuración DB
app.config.from_object('config.Config')
db.init_app(app)

# Healthcheck requerido por Consul
@app.route('/healthcheck')
def healthcheck():
    return '', 200

# Blueprint productos
app.register_blueprint(producto_controller)

if __name__ == '__main__':
    app.run()