from flask import Blueprint, request, jsonify
from ordenes.models.orden_model import Ordenes
from db.db import db
import requests
import os

orden_controller = Blueprint('orden_controller', __name__)
CONSUL_HOST = os.environ.get("CONSUL_HOST", "consul")


# 🔎 Función para descubrir servicios vía Consul
def get_service_address(service_name):
    response = requests.get(
    f"http://{CONSUL_HOST}:8500/v1/catalog/service/{service_name}"
    )

    services = response.json()

    if not services:
        raise Exception(f"Servicio {service_name} no encontrado")

    service = services[0]

    address = service['ServiceAddress'] or service['Address']
    port = service['ServicePort']

    return f"http://{address}:{port}"


# 🟢 Crear una nueva orden
@orden_controller.route('/api/ordenes', methods=['POST'])
def create_order():

    data = request.get_json()

    username = data.get('username')
    products = data.get('products')

    if not username:
        return jsonify({'message': 'Usuario requerido'}), 400

    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400

    users_service = get_service_address("users-service")

    if not users_service:
        return jsonify({'message': 'Servicio de usuarios no disponible'}), 503

    # Buscar usuario por username
    user_response = requests.get(f"{users_service}/api/users")

    if user_response.status_code != 200:
        return jsonify({'message': 'Error consultando usuarios'}), 500

    users = user_response.json()
    user = next((u for u in users if u['username'] == username), None)

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    user_email = user['email']

    products_service = get_service_address("products-service")
    

    if not products_service:
        return jsonify({'message': 'Servicio de productos no disponible'}), 503

    total = 0

    for item in products:

        product_id = item.get("id")
        quantity = item.get("quantity")

        if not product_id or not quantity:
            return jsonify({'message': 'Datos de producto inválidos'}), 400

        response = requests.get(f"{products_service}/api/productos/{product_id}")

        if response.status_code == 404:
            return jsonify({'message': f'Producto {product_id} no existe'}), 404

        product_data = response.json()

        if product_data['stock'] < quantity:
            return jsonify({'message': f'Inventario insuficiente para {product_data["nombre"]}'}), 409
        
        #Multiplicar la cantidad por el precio
        total += product_data['precio'] * quantity

        # Actualizar inventario
        update_response = requests.put(
            f"{products_service}/api/productos/{product_id}",
            json={
                "nombre": product_data["nombre"],
                "stock": product_data["stock"] - quantity,
                "precio": product_data["precio"]
            }
        )

        if update_response.status_code != 200:
            return jsonify({'message': 'Error actualizando inventario'}), 500

    new_order = Ordenes(
        nombre_usuario=username,
        correo=user_email,
        total=total
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        'message': 'Orden creada exitosamente',
        'total': total
    }), 201


# 🟢 Obtener todas las órdenes
@orden_controller.route('/api/ordenes', methods=['GET'])
def get_ordenes():
    ordenes = Ordenes.query.all()

    result = [
        {
            'id': orden.id,
            'nombre_usuario': orden.nombre_usuario,
            'correo': orden.correo,
            'total': orden.total
        }
        for orden in ordenes
    ]

    return jsonify(result)


# 🟢 Obtener una orden por id
@orden_controller.route('/api/ordenes/<int:orden_id>', methods=['GET'])
def get_orden(orden_id):
    orden = Ordenes.query.get_or_404(orden_id)

    return jsonify({
        'id': orden.id,
        'nombre_usuario': orden.nombre_usuario,
        'correo': orden.correo,
        'total': orden.total
    })