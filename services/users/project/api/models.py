from sqlalchemy.sql import func

from project import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellidos = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), default=True, nullable=False)
    direccion = db.Column(db.String(128), default=True, nullable=False)
    telefono = db.Column(db.String(128), default=True, nullable=False)
    dni = db.Column(db.String(128), default=True, nullable=False)
    ruc = db.Column(db.String(128), default=True, nullable=False)
    fecha_nacimiento = db.Column(db.String(128), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'email': self.email,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'dni': self.dni,
            'ruc': self.ruc,
            'fecha_nacimiento': self.fecha_nacimiento
        }

    def __init__(self, nombre, apellidos, email, direccion, telefono, dni, ruc,
     fecha_nacimiento):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.direccion = direccion
        self.telefono = telefono
        self.dni = dni
        self.ruc = ruc
        self.fecha_nacimiento = fecha_nacimiento