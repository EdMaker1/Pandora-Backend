from flask import Blueprint, request, jsonify
from services.ventas_service import VentaService
from schemas import VentaSchema

ventas_bp = Blueprint('ventas', __name__)
venta_schema = VentaSchema()
ventas_schema = VentaSchema(many=True)

@ventas_bp.route('/', methods=['GET'])
def listar_ventas():
    try:
        ventas = VentaService.obtener_todas()
        return jsonify(ventas_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:vid>', methods=['GET'])
def obtener_venta(vid):
    try:
        venta = VentaService.obtener_por_id(vid)
        return jsonify(venta_schema.dump(venta)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/', methods=['POST'])
def crear_venta():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Usar el servicio para crear venta con lógica transaccional
        venta = VentaService.crear_venta_transaccional(
            vendedor_id=data.get('vendedor_id'),
            cliente_id=data.get('cliente_id'),
            items_list=data.get('items', [])
        )
        
        return jsonify({
            'message': 'Venta creada correctamente',
            'venta': venta_schema.dump(venta)
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:vid>', methods=['PUT', 'PATCH'])
def actualizar_venta(vid):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        venta = VentaService.actualizar(vid, data)
        return jsonify(venta_schema.dump(venta)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:vid>', methods=['DELETE'])
def eliminar_venta(vid):
    try:
        VentaService.eliminar(vid)
        return jsonify({'message': 'Venta eliminada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def ventas_por_cliente(cliente_id):
    try:
        ventas = VentaService.obtener_por_cliente(cliente_id)
        return jsonify(ventas_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/vendedor/<int:vendedor_id>', methods=['GET'])
def ventas_por_vendedor(vendedor_id):
    try:
        ventas = VentaService.obtener_por_vendedor(vendedor_id)
        return jsonify(ventas_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500