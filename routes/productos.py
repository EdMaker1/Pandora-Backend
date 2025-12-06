from flask import Blueprint, request, jsonify
from services.productos_service import ProductoService
from schemas import ProductoSchema
from routes.auth import login_required, role_required

productos_bp = Blueprint('productos', __name__)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@productos_bp.route('/', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def listar_productos():
    try:
        activos_solo = request.args.get('activos', 'true').lower() == 'true'
        productos = ProductoService.obtener_todos(activos_solo=activos_solo)
        return jsonify(productos_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:pid>', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def obtener_producto(pid):
    try:
        producto = ProductoService.obtener_por_id(pid)
        return jsonify(producto_schema.dump(producto)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def crear_producto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        producto = ProductoService.crear(data)
        return jsonify(producto_schema.dump(producto)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:pid>', methods=['PUT', 'PATCH'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def actualizar_producto(pid):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        producto = ProductoService.actualizar(pid, data)
        return jsonify(producto_schema.dump(producto)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:pid>', methods=['DELETE'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'ALMACEN')
def eliminar_producto(pid):
    try:
        ProductoService.eliminar(pid)
        return jsonify({'message': 'Producto desactivado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:pid>/ajustar-stock', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'ALMACEN')
def ajustar_stock(pid):
    try:
        data = request.get_json()
        if not data or 'cantidad' not in data:
            return jsonify({'error': 'El campo "cantidad" es requerido'}), 400
        
        cantidad = data['cantidad']
        motivo = data.get('motivo', 'Ajuste manual')
        
        producto = ProductoService.ajustar_stock(pid, cantidad, motivo)
        return jsonify({
            'message': 'Stock ajustado correctamente',
            'producto': producto_schema.dump(producto)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/categoria/<int:categoria_id>', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def productos_por_categoria(categoria_id):
    try:
        productos = ProductoService.obtener_por_categoria(categoria_id)
        return jsonify(productos_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/buscar', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN')
def buscar_productos():
    termino = request.args.get('q', '')
    if not termino:
        return jsonify({'error': 'Parámetro "q" requerido'}), 400
    
    try:
        productos = ProductoService.buscar_por_nombre(termino)
        return jsonify(productos_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500