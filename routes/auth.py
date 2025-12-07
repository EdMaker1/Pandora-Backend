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
    
    session.permanent = True
    session['user_id'] = empleado.id
    session['username'] = empleado.username
    session['rol'] = empleado.rol
    session['nombre_completo'] = f"{empleado.primer_nombre} {empleado.apellido_paterno}"
    session['login_method'] = 'traditional'
    
    return jsonify({
        'message': 'Login exitoso',
        'user': {
            'id': empleado.id,
            'username': empleado.username,
            'rol': empleado.rol,
            'nombre_completo': session['nombre_completo'],
            'login_method': 'traditional'
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout exitoso'}), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    """Obtiene información del usuario autenticado (tradicional o Google OAuth)"""
    # Verificar si hay sesión
    if 'user_id' not in session:
        return jsonify({"error": "No autenticado"}), 401
    
    # Obtener información según el método de login
    login_method = session.get('login_method', 'traditional')
    
    if login_method == 'google':
        # Login con Google OAuth - datos ya están en sesión
        return jsonify({
            "id": session.get('user_id'),
            "username": session.get('username'),
            "rol": session.get('rol'),
            "nombre_completo": session.get('nombre_completo'),
            "picture": session.get('google_picture'),
            "login_method": "google"
        }), 200
    else:
        # Login tradicional - obtener de la base de datos
        empleado = Empleado.query.get(session['user_id'])
        
        if not empleado or not empleado.activo:
            session.clear()
            return jsonify({"error": "Usuario no encontrado o inactivo"}), 401
        
        return jsonify({
            "id": empleado.id,
            "username": empleado.username,
            "rol": empleado.rol,
            "nombre_completo": f"{empleado.primer_nombre} {empleado.apellido_paterno}",
            "picture": empleado.google_picture if empleado.google_picture else None,
            "login_method": "traditional"
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
                'nombre_completo': session.get('nombre_completo'),
                'login_method': session.get('login_method', 'traditional')
            }
        }), 200
    return jsonify({'authenticated': False}), 200