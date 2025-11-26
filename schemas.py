from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import Producto, Categoria, Empleado, Cliente, Venta, VentaItem, Pago, StockAdjustment

class CategoriaSchema(SQLAlchemySchema):
    class Meta:
        model = Categoria
        load_instance = True
    id = auto_field()
    nombre = auto_field()
    descripcion = auto_field()

class ProductoSchema(SQLAlchemySchema):
    class Meta:
        model = Producto
        load_instance = True
    id = auto_field()
    categoria_id = auto_field()
    nombre = auto_field()
    descripcion = auto_field()
    marca = auto_field()
    precio_venta_unitario = auto_field()
    precio_costo_unitario = auto_field()
    stock_actual = auto_field()
    stock_por_aumentar = auto_field()
    activo = auto_field()

class EmpleadoSchema(SQLAlchemySchema):
    class Meta:
        model = Empleado
        load_instance = True
    id = auto_field()
    primer_nombre = auto_field()
    segundo_nombre = auto_field()
    apellido_paterno = auto_field()
    apellido_materno = auto_field()
    username = auto_field()
    rol = auto_field()
    email = auto_field()
    activo = auto_field()

class ClienteSchema(SQLAlchemySchema):
    class Meta:
        model = Cliente
        load_instance = True
    id = auto_field()
    nombres = auto_field()
    apellidos = auto_field()
    email = auto_field()
    telefono = auto_field()
    direccion = auto_field()
    es_consumidor = auto_field()

class VentaItemSchema(SQLAlchemySchema):
    class Meta:
        model = VentaItem
        load_instance = True
    id = auto_field()
    venta_id = auto_field()
    producto_id = auto_field()
    cantidad = auto_field()
    precio_unitario = auto_field()
    subtotal_item = auto_field()

class VentaSchema(SQLAlchemySchema):
    class Meta:
        model = Venta
        load_instance = True
    id = auto_field()
    cliente_id = auto_field()
    vendedor_id = auto_field()
    fecha = auto_field()
    subtotal = auto_field()
    descuento_porcentual = auto_field()
    descuento_monto = auto_field()
    total = auto_field()
    estado = auto_field()
    items = auto_field()

class PagoSchema(SQLAlchemySchema):
    class Meta:
        model = Pago
        load_instance = True
    id = auto_field()
    venta_id = auto_field()
    monto = auto_field()
    metodo = auto_field()
    referencia = auto_field()
    fecha = auto_field()

class StockAdjustmentSchema(SQLAlchemySchema):
    class Meta:
        model = StockAdjustment
        load_instance = True
    id = auto_field()
    producto_id = auto_field()
    cantidad = auto_field()
    motivo = auto_field()
    registrado_por = auto_field()
    created_at = auto_field()