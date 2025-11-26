"""
Capa lógica para gestión de productos
"""
from models import db, Producto, Categoria
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

class ProductoService:
    
    @staticmethod
    def obtener_todos(activos_solo=True):
        """Obtiene todos los productos"""
        query = Producto.query
        if activos_solo:
            query = query.filter_by(activo=True)
        return query.all()
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por su ID"""
        producto = Producto.query.get(producto_id)
        if not producto:
            raise ValueError(f"Producto con ID {producto_id} no encontrado")
        return producto
    
    @staticmethod
    def crear(data):
        """
        Crea un nuevo producto
        :param data: dict con datos del producto
        :return: Producto creado
        """
        if not data.get('nombre'):
            raise ValueError("El campo 'nombre' es obligatorio")
        
        # Validar que la categoría exista
        if data.get('categoria_id'):
            categoria = Categoria.query.get(data['categoria_id'])
            if not categoria:
                raise ValueError(f"Categoría con ID {data['categoria_id']} no encontrada")
        
        # Validar precios
        precio_venta = Decimal(str(data.get('precio_venta_unitario', 0)))
        precio_costo = Decimal(str(data.get('precio_costo_unitario', 0)))
        
        if precio_venta < 0 or precio_costo < 0:
            raise ValueError("Los precios no pueden ser negativos")
        
        if precio_venta < precio_costo:
            raise ValueError("El precio de venta no puede ser menor al precio de costo")
        
        try:
            producto = Producto(
                categoria_id=data.get('categoria_id'),
                nombre=data['nombre'],
                descripcion=data.get('descripcion'),
                marca=data.get('marca'),
                precio_venta_unitario=precio_venta,
                precio_costo_unitario=precio_costo,
                stock_actual=data.get('stock_actual', 0),
                stock_por_aumentar=data.get('stock_por_aumentar', 0),
                activo=data.get('activo', True)
            )
            db.session.add(producto)
            db.session.commit()
            return producto
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear producto: {str(e)}")
    
    @staticmethod
    def actualizar(producto_id, data):
        """Actualiza un producto existente"""
        producto = ProductoService.obtener_por_id(producto_id)
        
        # Validar categoría si se está cambiando
        if data.get('categoria_id') and data['categoria_id'] != producto.categoria_id:
            categoria = Categoria.query.get(data['categoria_id'])
            if not categoria:
                raise ValueError(f"Categoría con ID {data['categoria_id']} no encontrada")
        
        # Validar precios si se proporcionan
        if 'precio_venta_unitario' in data or 'precio_costo_unitario' in data:
            precio_venta = Decimal(str(data.get('precio_venta_unitario', producto.precio_venta_unitario)))
            precio_costo = Decimal(str(data.get('precio_costo_unitario', producto.precio_costo_unitario)))
            
            if precio_venta < precio_costo:
                raise ValueError("El precio de venta no puede ser menor al precio de costo")
        
        try:
            if 'nombre' in data:
                producto.nombre = data['nombre']
            if 'descripcion' in data:
                producto.descripcion = data['descripcion']
            if 'marca' in data:
                producto.marca = data['marca']
            if 'categoria_id' in data:
                producto.categoria_id = data['categoria_id']
            if 'precio_venta_unitario' in data:
                producto.precio_venta_unitario = Decimal(str(data['precio_venta_unitario']))
            if 'precio_costo_unitario' in data:
                producto.precio_costo_unitario = Decimal(str(data['precio_costo_unitario']))
            if 'stock_actual' in data:
                producto.stock_actual = data['stock_actual']
            if 'stock_por_aumentar' in data:
                producto.stock_por_aumentar = data['stock_por_aumentar']
            if 'activo' in data:
                producto.activo = data['activo']
            
            db.session.commit()
            return producto
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar producto: {str(e)}")
    
    @staticmethod
    def eliminar(producto_id):
        """Desactiva un producto en lugar de eliminarlo físicamente"""
        producto = ProductoService.obtener_por_id(producto_id)
        
        try:
            producto.activo = False
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al desactivar producto: {str(e)}")
    
    @staticmethod
    def ajustar_stock(producto_id, cantidad, motivo="Ajuste manual"):
        """
        Ajusta el stock de un producto
        :param cantidad: puede ser positivo (añadir) o negativo (restar)
        """
        producto = ProductoService.obtener_por_id(producto_id)
        
        nuevo_stock = producto.stock_actual + cantidad
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        try:
            producto.stock_actual = nuevo_stock
            db.session.commit()
            return producto
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al ajustar stock: {str(e)}")
    
    @staticmethod
    def obtener_por_categoria(categoria_id):
        """Obtiene productos de una categoría específica"""
        return Producto.query.filter_by(categoria_id=categoria_id, activo=True).all()
    
    @staticmethod
    def buscar_por_nombre(termino):
        """Busca productos por nombre (búsqueda parcial)"""
        return Producto.query.filter(
            Producto.nombre.ilike(f'%{termino}%'),
            Producto.activo == True
        ).all()