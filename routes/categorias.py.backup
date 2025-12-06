from flask import Blueprint, request, jsonify
from services.categorias_service import CategoriaService
from schemas import CategoriaSchema

categorias_bp = Blueprint('categorias', __name__)
categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)

@categorias_bp.route('/', methods=['GET'])
def listar_categorias():
    try:
        categorias = CategoriaService.obtener_todas()
        return jsonify(categorias_schema.dump(categorias)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/<int:cid>', methods=['GET'])
def obtener_categoria(cid):
    try:
        categoria = CategoriaService.obtener_por_id(cid)
        return jsonify(categoria_schema.dump(categoria)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/', methods=['POST'])
def crear_categoria():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        categoria = CategoriaService.crear(data)
        return jsonify(categoria_schema.dump(categoria)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/<int:cid>', methods=['PUT', 'PATCH'])
def actualizar_categoria(cid):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        categoria = CategoriaService.actualizar(cid, data)
        return jsonify(categoria_schema.dump(categoria)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/<int:cid>', methods=['DELETE'])
def eliminar_categoria(cid):
    try:
        CategoriaService.eliminar(cid)
        return jsonify({'message': 'Categoría eliminada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/<int:cid>/productos/count', methods=['GET'])
def contar_productos_categoria(cid):
    try:
        cantidad = CategoriaService.contar_productos(cid)
        return jsonify({'categoria_id': cid, 'cantidad_productos': cantidad}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500