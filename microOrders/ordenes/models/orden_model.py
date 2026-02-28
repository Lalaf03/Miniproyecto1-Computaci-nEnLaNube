from db.db import db

class Ordenes(db.Model):
    __tablename__ = 'ordenes'

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __init__(self, nombre_usuario, correo, total):
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.total = total