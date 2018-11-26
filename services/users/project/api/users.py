

from flask import Blueprint, jsonify, request, render_template

from project.api.models import User
from project import db

from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    apellidos = post_data.get('apellidos')
    email = post_data.get('email')
    direccion = post_data.get('direccion')
    telefono = post_data.get('telefono')
    dni = post_data.get('dni')
    ruc = post_data.get('ruc')
    fecha_nacimiento = post_data.get('fecha_nacimiento')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(nombre=nombre, apellidos=apellidos,
             email=email, direccion=direccion, telefono=telefono, dni=dni,
              ruc=ruc, fecha_nacimiento=fecha_nacimiento))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{email} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Disculpe. Este email ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obteniendo detalles de un unico usuario"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Usuario no existe'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'apellidos': user.apellidos,
                    'email': user.email,
                    'direccion': user.direccion,
                    'telefono': user.telefono,
                    'dni': user.dni,
                    'ruc': user.ruc,
                    'fecha_nacimiento': user.fecha_nacimiento
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        dni = request.form['dni']
        ruc = request.form['ruc']
        fecha_nacimiento = request.form['fecha_nacimiento']
        db.session.add(User(
             nombre=nombre,
             apellidos=apellidos,
             email=email,
             direccion=direccion,
             telefono=telefono,
             dni=dni,
             ruc=ruc,
             fecha_nacimiento=fecha_nacimiento))
        db.session.commit()
    users = User.query.all()
    return render_template('register.html', users=users)