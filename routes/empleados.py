from flask import Blueprint, request, jsonify
from services.empleados_service import EmpleadoService
from schemas import EmpleadoSchema

empleados_bp = Blueprint('empleados', __name__)
empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)

@empleados_bp.route('/', methods=['GET'])
def listar_empleados():
    try:
        activos_solo = request.args.get('activos', 'true').lower() == 'true'
        empleados = EmpleadoService.obtener_todos(activos_solo=activos_solo)
        return jsonify(empleados_schema.dump(empleados)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['GET'])
def obtener_empleado(eid):
    try:
        empleado = EmpleadoService.obtener_por_id(eid)
        return jsonify(empleado_schema.dump(empleado)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/', methods=['POST'])
def crear_empleado():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        empleado = EmpleadoService.crear(data)
        return jsonify(empleado_schema.dump(empleado)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['PUT', 'PATCH'])
def actualizar_empleado(eid):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        empleado = EmpleadoService.actualizar(eid, data)
        return jsonify(empleado_schema.dump(empleado)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:eid>', methods=['DELETE'])
def eliminar_empleado(eid):
    try:
        EmpleadoService.eliminar(eid)
        return jsonify({'message': 'Empleado desactivado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/username/<username>', methods=['GET'])
def buscar_por_username(username):
    try:
        empleado = EmpleadoService.buscar_por_username(username)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify(empleado_schema.dump(empleado)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/rol/<rol>', methods=['GET'])
def listar_por_rol(rol):
    try:
        empleados = EmpleadoService.obtener_por_rol(rol)
        return jsonify(empleados_schema.dump(empleados)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500