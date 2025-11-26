from flask import Blueprint, jsonify
from models import db, Venta, Producto, Cliente
from schemas import VentaSchema, ProductoSchema, ClienteSchema
from sqlalchemy import func

reportes_bp = Blueprint('reportes', __name__)

venta_schema = VentaSchema(many=True)
producto_schema = ProductoSchema(many=True)
cliente_schema = ClienteSchema(many=True)

@reportes_bp.route('/ventas', methods=['GET'])
def reporte_ventas():
    try:
        ventas = Venta.query.order_by(Venta.fecha.desc()).all()
        return jsonify(venta_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/productos', methods=['GET'])
def reporte_productos():
    try:
        productos = Producto.query.filter_by(activo=True).all()
        return jsonify(producto_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/clientes', methods=['GET'])
def reporte_clientes():
    try:
        clientes = Cliente.query.all()
        return jsonify(cliente_schema.dump(clientes)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/resumen', methods=['GET'])
def reporte_resumen():
    try:
        total_ventas = db.session.query(func.sum(Venta.total)).scalar() or 0
        total_clientes = db.session.query(func.count(Cliente.id)).scalar()
        total_productos = db.session.query(func.count(Producto.id)).filter(Producto.activo == True).scalar()
        cantidad_ventas = db.session.query(func.count(Venta.id)).scalar()
        
        return jsonify({
            'total_ventas': float(total_ventas),
            'cantidad_ventas': cantidad_ventas,
            'total_clientes': total_clientes,
            'total_productos': total_productos
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/productos-bajo-stock', methods=['GET'])
def productos_bajo_stock():
    try:
        limite = 10  # Puedes hacerlo configurable
        productos = Producto.query.filter(
            Producto.stock_actual <= limite,
            Producto.activo == True
        ).all()
        return jsonify(producto_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/top-productos', methods=['GET'])
def top_productos_vendidos():
    try:
        # Esta query requeriría unir con VentaItem para calcular productos más vendidos
        # Por ahora retornamos productos ordenados por stock (ejemplo)
        productos = Producto.query.filter_by(activo=True).order_by(Producto.stock_actual.desc()).limit(10).all()
        return jsonify(producto_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500