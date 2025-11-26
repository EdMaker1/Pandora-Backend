from flask import Blueprint, request, jsonify
from models import db, Pago
from schemas import PagoSchema

pagos_bp = Blueprint('pagos', __name__)
pago_schema = PagoSchema()
pagos_schema = PagoSchema(many=True)

@pagos_bp.route('/', methods=['GET'])
def listar_pagos():
    try:
        pagos = Pago.query.all()
        return jsonify(pagos_schema.dump(pagos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['GET'])
def obtener_pago(pid):
    try:
        pago = Pago.query.get_or_404(pid)
        return jsonify(pago_schema.dump(pago)), 200
    except Exception as e:
        return jsonify({'error': 'Pago no encontrado'}), 404

@pagos_bp.route('/', methods=['POST'])
def crear_pago():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        required = ['venta_id', 'monto']
        for r in required:
            if r not in data:
                return jsonify({'error': f'{r} es requerido'}), 400
        
        pago = Pago(
            venta_id=data['venta_id'],
            monto=data['monto'],
            metodo=data.get('metodo'),
            referencia=data.get('referencia'),
            cliente=data.get('cliente'),
            telefono=data.get('telefono')
        )
        db.session.add(pago)
        db.session.commit()
        return jsonify(pago_schema.dump(pago)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['PUT', 'PATCH'])
def actualizar_pago(pid):
    try:
        pago = Pago.query.get_or_404(pid)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        for key in ['venta_id', 'monto', 'metodo', 'referencia', 'cliente', 'telefono']:
            if key in data:
                setattr(pago, key, data[key])
        
        db.session.commit()
        return jsonify(pago_schema.dump(pago)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['DELETE'])
def eliminar_pago(pid):
    try:
        pago = Pago.query.get_or_404(pid)
        db.session.delete(pago)
        db.session.commit()
        return jsonify({'message': 'Pago eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/venta/<int:venta_id>', methods=['GET'])
def pagos_por_venta(venta_id):
    try:
        pagos = Pago.query.filter_by(venta_id=venta_id).all()
        return jsonify(pagos_schema.dump(pagos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500