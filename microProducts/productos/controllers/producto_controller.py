from flask import Blueprint, request, jsonify
from productos.models.producto_model import Productos
from db.db import db

producto_controller = Blueprint('producto_controller', __name__)

# Obtener todos los productos
@producto_controller.route('/api/productos', methods=['GET'])
def get_productos():
    print("listado de productos")
    productos = Productos.query.all()
    result = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock
        }
        for producto in productos
    ]
    return jsonify(result)

# Obtener un producto por id
@producto_controller.route('/api/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    print("obteniendo producto")
    producto = Productos.query.get_or_404(producto_id)
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'stock': producto.stock
    })

# Crear un nuevo producto
@producto_controller.route('/api/productos', methods=['POST'])
def create_producto():
    print("creando producto")
    data = request.json

    new_producto = Productos(
        nombre=data['nombre'],
        precio=data['precio'],
        stock=data['stock']
    )

    db.session.add(new_producto)
    db.session.commit()

    return jsonify({'message': 'Producto creado exitosamente'}), 201

# Actualizar un producto existente
@producto_controller.route('/api/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    print("actualizando producto")
    producto = Productos.query.get_or_404(producto_id)
    data = request.json

    producto.nombre = data['nombre']
    producto.precio = data['precio']
    producto.stock = data['stock']

    db.session.commit()

    return jsonify({'message': 'Producto actualizado exitosamente'})

# Eliminar un producto
@producto_controller.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    print("eliminando producto")
    producto = Productos.query.get_or_404(producto_id)

    db.session.delete(producto)
    db.session.commit()

    return jsonify({'message': 'Producto eliminado exitosamente'})