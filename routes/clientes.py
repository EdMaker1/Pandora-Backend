"""
Blueprint de rutas para clientes
Usa la capa de servicios para la lógica de negocio
"""
from flask import Blueprint, jsonify, request
from services.clientes_service import ClienteService

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes"""
    try:
        clientes = ClienteService.obtener_todos()
        resultado = [ClienteService.serializar(c) for c in clientes]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    """Obtener cliente por ID"""
    try:
        cliente = ClienteService.obtener_por_id(id)
        return jsonify(ClienteService.serializar(cliente)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@clientes_bp.route('/', methods=['POST'])
def add_cliente():
    """Crear nuevo cliente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        cliente = ClienteService.crear(data)
        return jsonify({
            "message": "Cliente creado correctamente",
            "cliente": ClienteService.serializar(cliente)
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@clientes_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_cliente(id):
    """Actualizar cliente existente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        cliente = ClienteService.actualizar(id, data)
        return jsonify({
            "message": "Cliente actualizado correctamente",
            "cliente": ClienteService.serializar(cliente)
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    """Eliminar cliente"""
    try:
        ClienteService.eliminar(id)
        return jsonify({"message": "Cliente eliminado correctamente"}), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@clientes_bp.route('/buscar', methods=['GET'])
def buscar_cliente():
    """Buscar cliente por email"""
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Parámetro 'email' requerido"}), 400
    
    try:
        cliente = ClienteService.buscar_por_email(email)
        if not cliente:
            return jsonify({"message": "Cliente no encontrado"}), 404
        return jsonify(ClienteService.serializar(cliente)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500