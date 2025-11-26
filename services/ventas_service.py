"""
Capa lógica para gestión de ventas
"""
from models import db, Producto, Venta, VentaItem, Cliente, Setting
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

class VentaService:
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las ventas"""
        try:
            return Venta.query.order_by(Venta.fecha.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener ventas: {str(e)}")
    
    @staticmethod
    def obtener_por_id(venta_id):
        """Obtiene una venta por su ID"""
        venta = Venta.query.get(venta_id)
        if not venta:
            raise ValueError(f"Venta con ID {venta_id} no encontrada")
        return venta
    
    @staticmethod
    def crear_venta_transaccional(vendedor_id, cliente_id, items_list):
        """
        Crea una venta completa con sus items de forma transaccional
        :param vendedor_id: ID del empleado vendedor
        :param cliente_id: ID del cliente (puede ser None)
        :param items_list: [{'producto_id': int, 'cantidad': int}, ...]
        :return: Venta creada
        """
        if not vendedor_id:
            raise ValueError("El campo 'vendedor_id' es requerido")
        
        if not items_list or len(items_list) == 0:
            raise ValueError("Debe incluir al menos un producto en la venta")
        
        try:
            subtotal = Decimal('0.00')
            productos_cache = {}
            
            # Validar productos y calcular subtotal
            for it in items_list:
                pid = int(it['producto_id'])
                cant = int(it['cantidad'])
                
                if cant <= 0:
                    raise ValueError(f"La cantidad debe ser mayor a 0")
                
                prod = Producto.query.get(pid)
                if not prod:
                    raise ValueError(f"Producto {pid} no existe")
                
                if not prod.activo:
                    raise ValueError(f"Producto {prod.nombre} no está activo")
                
                if prod.stock_actual < cant:
                    raise ValueError(f"Stock insuficiente para producto {prod.nombre}. Disponible: {prod.stock_actual}")
                
                productos_cache[pid] = prod
                subtotal += Decimal(prod.precio_venta_unitario) * cant
            
            # Calcular descuento por consumidor
            descuento_pct = Decimal('0.00')
            if cliente_id:
                cliente = Cliente.query.get(cliente_id)
                if cliente and cliente.es_consumidor:
                    s = Setting.query.filter_by(key='descuento_consumidor_porcentual').first()
                    if s and s.value:
                        descuento_pct = Decimal(s.value)
            
            descuento_monto = (subtotal * descuento_pct) / Decimal(100)
            total = subtotal - descuento_monto
            
            # Crear venta
            venta = Venta(
                cliente_id=cliente_id,
                vendedor_id=vendedor_id,
                subtotal=subtotal,
                descuento_porcentual=descuento_pct,
                descuento_monto=descuento_monto,
                total=total,
                estado='COMPLETADA'
            )
            db.session.add(venta)
            db.session.flush()  # para obtener venta.id
            
            # Crear items y actualizar stock
            for it in items_list:
                pid = int(it['producto_id'])
                cant = int(it['cantidad'])
                prod = productos_cache[pid]
                
                item = VentaItem(
                    venta_id=venta.id,
                    producto_id=pid,
                    cantidad=cant,
                    precio_unitario=prod.precio_venta_unitario,
                    subtotal_item=Decimal(prod.precio_venta_unitario) * cant
                )
                db.session.add(item)
                
                # Actualizar stock
                prod.stock_actual = prod.stock_actual - cant
                db.session.add(prod)
            
            db.session.commit()
            return venta
            
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def actualizar(venta_id, data):
        """Actualiza una venta existente (solo campos permitidos)"""
        venta = VentaService.obtener_por_id(venta_id)
        
        try:
            if 'estado' in data:
                venta.estado = data['estado']
            
            db.session.commit()
            return venta
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar venta: {str(e)}")
    
    @staticmethod
    def eliminar(venta_id):
        """
        Elimina una venta (solo si no tiene pagos asociados)
        Restaura el stock de los productos
        """
        venta = VentaService.obtener_por_id(venta_id)
        
        # Validar que no tenga pagos
        if venta.pagos:
            raise ValueError("No se puede eliminar una venta con pagos registrados")
        
        try:
            # Restaurar stock de productos
            for item in venta.items:
                producto = Producto.query.get(item.producto_id)
                if producto:
                    producto.stock_actual = producto.stock_actual + item.cantidad
                    db.session.add(producto)
            
            # Eliminar items
            for item in venta.items:
                db.session.delete(item)
            
            # Eliminar venta
            db.session.delete(venta)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar venta: {str(e)}")
    
    @staticmethod
    def obtener_por_cliente(cliente_id):
        """Obtiene ventas de un cliente específico"""
        return Venta.query.filter_by(cliente_id=cliente_id).order_by(Venta.fecha.desc()).all()
    
    @staticmethod
    def obtener_por_vendedor(vendedor_id):
        """Obtiene ventas de un vendedor específico"""
        return Venta.query.filter_by(vendedor_id=vendedor_id).order_by(Venta.fecha.desc()).all()