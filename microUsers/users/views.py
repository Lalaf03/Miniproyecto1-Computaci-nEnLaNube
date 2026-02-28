from flask import Flask
from users.controllers.user_controller import user_controller
from db.db import db
from flask_cors import CORS
from flask_consulate import Consul
import os

app = Flask(__name__)
CORS(app)

# -------- CONSUL --------
CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "users-service")
SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 5002))
SERVICE_HOST = os.environ.get("SERVICE_HOST", "microusers")

consul = Consul(app=app, host=CONSUL_HOST)

consul.register_service(
    name=SERVICE_NAME,
    interval='5s',
    tags=['users', 'flask'],
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

app.secret_key = "super_secret_key"

# Blueprint usuarios
app.register_blueprint(user_controller)

if __name__ == '__main__':
    app.run()