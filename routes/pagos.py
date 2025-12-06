from flask import Blueprint, request, jsonify
from models import db, Pago
from schemas import PagoSchema
from routes.auth import login_required, role_required

pagos_bp = Blueprint('pagos', __name__)
pago_schema = PagoSchema()
pagos_schema = PagoSchema(many=True)

@pagos_bp.route('/', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')  # Solo ADMIN y SOPORTE
def listar_pagos():
    """Lista todos los pagos"""
    try:
        pagos = Pago.query.order_by(Pago.fecha.desc()).all()
        return jsonify(pagos_schema.dump(pagos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def obtener_pago(pid):
    """Obtiene un pago por ID"""
    try:
        pago = Pago.query.get_or_404(pid)
        return jsonify(pago_schema.dump(pago)), 200
    except Exception as e:
        return jsonify({'error': 'Pago no encontrado'}), 404

@pagos_bp.route('/', methods=['POST'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def crear_pago():
    """Registra un nuevo pago"""
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
        return jsonify({
            'message': 'Pago registrado exitosamente',
            'pago': pago_schema.dump(pago)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['PUT', 'PATCH'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def actualizar_pago(pid):
    """Actualiza un pago existente"""
    try:
        pago = Pago.query.get_or_404(pid)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        for key in ['venta_id', 'monto', 'metodo', 'referencia', 'cliente', 'telefono']:
            if key in data:
                setattr(pago, key, data[key])
        
        db.session.commit()
        return jsonify({
            'message': 'Pago actualizado exitosamente',
            'pago': pago_schema.dump(pago)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/<int:pid>', methods=['DELETE'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')  # Solo ADMIN puede eliminar
def eliminar_pago(pid):
    """Elimina un pago"""
    try:
        pago = Pago.query.get_or_404(pid)
        db.session.delete(pago)
        db.session.commit()
        return jsonify({'message': 'Pago eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/venta/<int:venta_id>', methods=['GET'])
@login_required
def pagos_por_venta(venta_id):
    """Lista pagos de una venta específica"""
    try:
        pagos = Pago.query.filter_by(venta_id=venta_id).all()
        return jsonify(pagos_schema.dump(pagos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500