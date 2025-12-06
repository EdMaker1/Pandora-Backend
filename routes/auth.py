from flask import Blueprint, request, jsonify, session
from models import db, Empleado
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'No autenticado'}), 401
            empleado = Empleado.query.get(session['user_id'])
            if not empleado or empleado.rol not in roles:
                return jsonify({'error': 'Sin permisos'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username y password requeridos'}), 400
    
    empleado = Empleado.query.filter_by(username=data['username'], activo=True).first()
    if not empleado or not empleado.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    session['user_id'] = empleado.id
    session['username'] = empleado.username
    session['rol'] = empleado.rol
    session['nombre_completo'] = f"{empleado.primer_nombre} {empleado.apellido_paterno}"
    
    return jsonify({
        'message': 'Login exitoso',
        'user': {
            'id': empleado.id,
            'username': empleado.username,
            'rol': empleado.rol,
            'nombre_completo': session['nombre_completo']
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout exitoso'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    empleado = Empleado.query.get(session['user_id'])
    if not empleado:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({
        'id': empleado.id,
        'username': empleado.username,
        'rol': empleado.rol,
        'nombre_completo': f"{empleado.primer_nombre} {empleado.apellido_paterno}"
    }), 200

@auth_bp.route('/check', methods=['GET'])
def check():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'rol': session['rol'],
                'nombre_completo': session.get('nombre_completo')
            }
        }), 200
    return jsonify({'authenticated': False}), 200