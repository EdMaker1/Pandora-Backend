from flask import Blueprint, request, jsonify
from models import db, StockAdjustment
from schemas import StockAdjustmentSchema

stock_bp = Blueprint('stock_adjustment', __name__)
stock_schema = StockAdjustmentSchema()
stocks_schema = StockAdjustmentSchema(many=True)

@stock_bp.route('/', methods=['GET'])
def listar_ajustes():
    try:
        ajustes = StockAdjustment.query.order_by(StockAdjustment.created_at.desc()).all()
        return jsonify(stocks_schema.dump(ajustes)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/<int:sid>', methods=['GET'])
def obtener_ajuste(sid):
    try:
        ajuste = StockAdjustment.query.get_or_404(sid)
        return jsonify(stock_schema.dump(ajuste)), 200
    except Exception as e:
        return jsonify({'error': 'Ajuste no encontrado'}), 404

@stock_bp.route('/', methods=['POST'])
def crear_ajuste():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        required = ['producto_id', 'cantidad', 'motivo']
        for r in required:
            if r not in data:
                return jsonify({'error': f'{r} es requerido'}), 400
        
        ajuste = StockAdjustment(
            producto_id=data['producto_id'],
            cantidad=data['cantidad'],
            motivo=data['motivo'],
            registrado_por=data.get('registrado_por')
        )
        db.session.add(ajuste)
        db.session.commit()
        return jsonify(stock_schema.dump(ajuste)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/<int:sid>', methods=['PUT', 'PATCH'])
def actualizar_ajuste(sid):
    try:
        ajuste = StockAdjustment.query.get_or_404(sid)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        for key in ['producto_id', 'cantidad', 'motivo', 'registrado_por']:
            if key in data:
                setattr(ajuste, key, data[key])
        
        db.session.commit()
        return jsonify(stock_schema.dump(ajuste)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/<int:sid>', methods=['DELETE'])
def eliminar_ajuste(sid):
    try:
        ajuste = StockAdjustment.query.get_or_404(sid)
        db.session.delete(ajuste)
        db.session.commit()
        return jsonify({'message': 'Ajuste de stock eliminado correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/producto/<int:producto_id>', methods=['GET'])
def ajustes_por_producto(producto_id):
    try:
        ajustes = StockAdjustment.query.filter_by(producto_id=producto_id).order_by(StockAdjustment.created_at.desc()).all()
        return jsonify(stocks_schema.dump(ajustes)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500