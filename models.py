from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    marca = db.Column(db.String(100), nullable=True)
    precio_venta_unitario = db.Column(db.Numeric(12,2), nullable=False, default=0)
    precio_costo_unitario = db.Column(db.Numeric(12,2), nullable=False, default=0)
    stock_actual = db.Column(db.Integer, default=0)
    stock_por_aumentar = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Empleado(db.Model):
    __tablename__='empleado'
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(80), nullable=False)
    segundo_nombre = db.Column(db.String(80), nullable=True)
    apellido_paterno = db.Column(db.String(80), nullable=False)
    apellido_materno = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable para usuarios de Google
    rol = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos para Google OAuth
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    google_email = db.Column(db.String(255), nullable=True)
    google_picture = db.Column(db.String(512), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

class Cliente(db.Model):
    __tablename__='cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150), nullable=False)
    apellidos = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True, unique=True)
    telefono = db.Column(db.String(30), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    es_consumidor = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Venta(db.Model):
    __tablename__='venta'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    vendedor = db.relationship('Empleado', backref=db.backref('ventas', lazy=True))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(12,2), nullable=False, default=0)
    descuento_porcentual = db.Column(db.Numeric(5,2), default=0)
    descuento_monto = db.Column(db.Numeric(12,2), default=0)
    total = db.Column(db.Numeric(12,2), nullable=False, default=0)
    estado = db.Column(db.String(20), default='COMPLETADA')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VentaItem(db.Model):
    __tablename__='venta_item'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    venta = db.relationship('Venta', backref=db.backref('items', lazy=True))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto')
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(12,2), nullable=False)
    subtotal_item = db.Column(db.Numeric(12,2), nullable=False)

class Pago(db.Model):
    __tablename__='pago'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    venta = db.relationship('Venta', backref=db.backref('pagos', lazy=True))
    monto = db.Column(db.Numeric(12,2), nullable=False)
    metodo = db.Column(db.String(50), nullable=True)
    referencia = db.Column(db.String(100), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class StockAdjustment(db.Model):
    __tablename__ = 'stock_adjustment'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto')
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(100), nullable=True)
    registrado_por = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    __tablename__='setting'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)