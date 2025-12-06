from flask import Blueprint, request, jsonify
from services.empleados_service import EmpleadoService
from schemas import EmpleadoSchema
from routes.auth import login_required, role_required

empleados_bp = Blueprint('empleados', __name__)
empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)

@empleados_bp.route('/', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO')  # Solo ADMINISTRADOR y SOPORTE pueden ver empleados
def listar_empleados():
    """Lista todos los empleados (requiere rol ADMINISTRADOR o SOPORTE)"""
    try:
        activos_solo = request.args.get('activos', 'true').lower() == 'true'
        empleados = EmpleadoService.obtener_todos(activos_solo=activos_solo)
        return jsonify(empleados_schema.dump(empleados)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE')
def obtener_empleado(eid):
    """Obtiene un empleado por ID"""
    try:
        empleado = EmpleadoService.obtener_por_id(eid)
        return jsonify(empleado_schema.dump(empleado)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE')
def crear_empleado():
    """Crea un nuevo empleado (requiere password en el body)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        empleado = EmpleadoService.crear(data)
        return jsonify({
            'message': 'Empleado creado exitosamente',
            'empleado': EmpleadoService.serializar(empleado)
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['PUT', 'PATCH'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE')
def actualizar_empleado(eid):
    """Actualiza un empleado existente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        empleado = EmpleadoService.actualizar(eid, data)
        return jsonify({
            'message': 'Empleado actualizado exitosamente',
            'empleado': EmpleadoService.serializar(empleado)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['DELETE'])
@login_required
@role_required('ADMINISTRADOR')  # Solo ADMINISTRADOR puede eliminar
def eliminar_empleado(eid):
    """Desactiva un empleado"""
    try:
        EmpleadoService.eliminar(eid)
        return jsonify({'message': 'Empleado desactivado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/username/<username>', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE')
def buscar_por_username(username):
    """Busca empleado por username"""
    try:
        empleado = EmpleadoService.buscar_por_username(username)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify(EmpleadoService.serializar(empleado)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/rol/<rol>', methods=['GET'])
@login_required
def listar_por_rol(rol):
    """Lista empleados por rol"""
    try:
        empleados = EmpleadoService.obtener_por_rol(rol)
        return jsonify(empleados_schema.dump(empleados)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500