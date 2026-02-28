from flask import Flask
from ordenes.controllers.orden_controller import orden_controller
from db.db import db
from flask_cors import CORS
from flask_consulate import Consul
import os

app = Flask(__name__)
CORS(app)

# ===== CONFIG CONSUL =====
CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "orders-service")
SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 5004))
SERVICE_HOST = os.environ.get("SERVICE_HOST", "microorders")

consul = Consul(app=app, host=CONSUL_HOST)

consul.register_service(
    name=SERVICE_NAME,
    interval='5s',
    tags=['orders', 'flask'],
    port=SERVICE_PORT,
    httpcheck=f'http://{SERVICE_HOST}:{SERVICE_PORT}/healthcheck'
)

# ===== CONFIG DB =====
app.config.from_object('config.Config')
db.init_app(app)

# ===== HEALTHCHECK =====
@app.route('/healthcheck')
def healthcheck():
    return '', 200

# ===== CONTROLLER =====
app.register_blueprint(orden_controller)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVICE_PORT)