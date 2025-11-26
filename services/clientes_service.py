"""
Capa lógica para gestión de clientes
"""
from models import db, Cliente
from sqlalchemy.exc import SQLAlchemyError

class ClienteService:
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los clientes activos"""
        try:
            return Cliente.query.all()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener clientes: {str(e)}")
    
    @staticmethod
    def obtener_por_id(cliente_id):
        """Obtiene un cliente por su ID"""
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")
        return cliente
    
    @staticmethod
    def crear(data):
        """
        Crea un nuevo cliente
        :param data: dict con nombres, apellidos, email, telefono, direccion
        :return: Cliente creado
        """
        if not data.get('nombres'):
            raise ValueError("El campo 'nombres' es obligatorio")
        
        # Validar email único si se proporciona
        if data.get('email'):
            existe = Cliente.query.filter_by(email=data['email']).first()
            if existe:
                raise ValueError(f"El email {data['email']} ya está registrado")
        
        try:
            nuevo_cliente = Cliente(
                nombres=data.get('nombres'),
                apellidos=data.get('apellidos'),
                email=data.get('email'),
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                es_consumidor=data.get('es_consumidor', False)
            )
            db.session.add(nuevo_cliente)
            db.session.commit()
            return nuevo_cliente
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear cliente: {str(e)}")
    
    @staticmethod
    def actualizar(cliente_id, data):
        """
        Actualiza un cliente existente
        :param cliente_id: ID del cliente
        :param data: dict con campos a actualizar
        :return: Cliente actualizado
        """
        cliente = ClienteService.obtener_por_id(cliente_id)
        
        # Validar email único si se está cambiando
        if data.get('email') and data['email'] != cliente.email:
            existe = Cliente.query.filter_by(email=data['email']).first()
            if existe:
                raise ValueError(f"El email {data['email']} ya está registrado")
        
        try:
            cliente.nombres = data.get('nombres', cliente.nombres)
            cliente.apellidos = data.get('apellidos', cliente.apellidos)
            cliente.email = data.get('email', cliente.email)
            cliente.telefono = data.get('telefono', cliente.telefono)
            cliente.direccion = data.get('direccion', cliente.direccion)
            cliente.es_consumidor = data.get('es_consumidor', cliente.es_consumidor)
            
            db.session.commit()
            return cliente
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar cliente: {str(e)}")
    
    @staticmethod
    def eliminar(cliente_id):
        """
        Elimina un cliente (validando que no tenga ventas)
        :param cliente_id: ID del cliente
        """
        cliente = ClienteService.obtener_por_id(cliente_id)
        
        # Validar que no tenga ventas asociadas
        if cliente.ventas:
            raise ValueError("No se puede eliminar un cliente con ventas registradas")
        
        try:
            db.session.delete(cliente)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar cliente: {str(e)}")
    
    @staticmethod
    def buscar_por_email(email):
        """Busca un cliente por email"""
        return Cliente.query.filter_by(email=email).first()
    
    @staticmethod
    def serializar(cliente):
        """Serializa un cliente a diccionario"""
        return {
            "id": cliente.id,
            "nombres": cliente.nombres,
            "apellidos": cliente.apellidos,
            "email": cliente.email,
            "telefono": cliente.telefono,
            "direccion": cliente.direccion,
            "es_consumidor": cliente.es_consumidor,
            "created_at": cliente.created_at.isoformat() if cliente.created_at else None
        }