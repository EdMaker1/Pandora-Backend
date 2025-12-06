from flask import Blueprint, jsonify, request
from models import db, Venta, Producto, Cliente, VentaItem
from schemas import VentaSchema, ProductoSchema, ClienteSchema
from sqlalchemy import func
from routes.auth import login_required, role_required

reportes_bp = Blueprint('reportes', __name__)

venta_schema = VentaSchema(many=True)
producto_schema = ProductoSchema(many=True)
cliente_schema = ClienteSchema(many=True)

@reportes_bp.route('/ventas', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def reporte_ventas():
    """Reporte completo de ventas"""
    try:
        ventas = Venta.query.order_by(Venta.fecha.desc()).all()
        return jsonify(venta_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/productos', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def reporte_productos():
    """Reporte de productos activos"""
    try:
        productos = Producto.query.filter_by(activo=True).all()
        return jsonify(producto_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/clientes', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def reporte_clientes():
    """Reporte de clientes"""
    try:
        clientes = Cliente.query.all()
        return jsonify(cliente_schema.dump(clientes)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/resumen', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def reporte_resumen():
    """Dashboard con métricas principales"""
    try:
        total_ventas = db.session.query(func.sum(Venta.total)).scalar() or 0
        total_clientes = db.session.query(func.count(Cliente.id)).scalar()
        total_productos = db.session.query(func.count(Producto.id)).filter(Producto.activo == True).scalar()
        cantidad_ventas = db.session.query(func.count(Venta.id)).scalar()
        
        # Productos más vendidos
        productos_vendidos = db.session.query(
            Producto.nombre,
            func.sum(VentaItem.cantidad).label('total_vendido')
        ).join(VentaItem).group_by(Producto.id).order_by(func.sum(VentaItem.cantidad).desc()).limit(5).all()
        
        return jsonify({
            'total_ventas': float(total_ventas),
            'cantidad_ventas': cantidad_ventas,
            'total_clientes': total_clientes,
            'total_productos': total_productos,
            'productos_top': [{'nombre': p[0], 'cantidad': int(p[1])} for p in productos_vendidos]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/productos-bajo-stock', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def productos_bajo_stock():
    """Productos con stock bajo"""
    try:
        limite = int(request.args.get('limite', 10))
        productos = Producto.query.filter(
            Producto.stock_actual <= limite,
            Producto.activo == True
        ).all()
        return jsonify(producto_schema.dump(productos)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/ventas-por-periodo', methods=['GET'])
@login_required
@role_required('ADMINISTRADOR', 'SOPORTE', 'CAJERO')
def ventas_por_periodo():
    """Ventas agrupadas por fecha"""
    try:
        # Ventas de los últimos 30 días agrupadas por día
        ventas_por_dia = db.session.query(
            func.date(Venta.fecha).label('fecha'),
            func.count(Venta.id).label('cantidad'),
            func.sum(Venta.total).label('total')
        ).group_by(func.date(Venta.fecha)).order_by(func.date(Venta.fecha).desc()).limit(30).all()
        
        return jsonify([{
            'fecha': str(v[0]),
            'cantidad': v[1],
            'total': float(v[2])
        } for v in ventas_por_dia]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500