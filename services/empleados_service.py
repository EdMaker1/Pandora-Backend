"""
Capa lógica para gestión de empleados
"""
from models import db, Empleado
from sqlalchemy.exc import SQLAlchemyError

class EmpleadoService:
    
    # Roles válidos del sistema
    ROLES_VALIDOS = ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN']
    
    @staticmethod
    def obtener_todos(activos_solo=True):
        """Obtiene todos los empleados"""
        query = Empleado.query
        if activos_solo:
            query = query.filter_by(activo=True)
        return query.all()
    
    @staticmethod
    def obtener_por_id(empleado_id):
        """Obtiene un empleado por su ID"""
        empleado = Empleado.query.get(empleado_id)
        if not empleado:
            raise ValueError(f"Empleado con ID {empleado_id} no encontrado")
        return empleado
    
    @staticmethod
    def crear(data):
        """
        Crea un nuevo empleado
        :param data: dict con datos del empleado (incluye password)
        :return: Empleado creado
        """
        # Validaciones obligatorias
        if not data.get('primer_nombre'):
            raise ValueError("El campo 'primer_nombre' es obligatorio")
        
        if not data.get('apellido_paterno'):
            raise ValueError("El campo 'apellido_paterno' es obligatorio")
        
        if not data.get('username'):
            raise ValueError("El campo 'username' es obligatorio")
        
        if not data.get('password'):
            raise ValueError("El campo 'password' es obligatorio")
        
        if not data.get('rol'):
            raise ValueError("El campo 'rol' es obligatorio")
        
        # Validar rol
        if data['rol'] not in EmpleadoService.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(EmpleadoService.ROLES_VALIDOS)}")
        
        # Validar username único
        existe = Empleado.query.filter_by(username=data['username']).first()
        if existe:
            raise ValueError(f"El username '{data['username']}' ya está registrado")
        
        # Validar email único si se proporciona
        if data.get('email'):
            existe = Empleado.query.filter_by(email=data['email']).first()
            if existe:
                raise ValueError(f"El email {data['email']} ya está registrado")
        
        # Validar longitud de contraseña
        if len(data['password']) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        
        try:
            empleado = Empleado(
                primer_nombre=data['primer_nombre'],
                segundo_nombre=data.get('segundo_nombre'),
                apellido_paterno=data['apellido_paterno'],
                apellido_materno=data.get('apellido_materno'),
                username=data['username'],
                rol=data['rol'],
                email=data.get('email'),
                activo=data.get('activo', True)
            )
            empleado.set_password(data['password'])
            
            db.session.add(empleado)
            db.session.commit()
            return empleado
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear empleado: {str(e)}")
    
    @staticmethod
    def actualizar(empleado_id, data):
        """Actualiza un empleado existente"""
        empleado = EmpleadoService.obtener_por_id(empleado_id)
        
        # Validar username único si se está cambiando
        if data.get('username') and data['username'] != empleado.username:
            existe = Empleado.query.filter_by(username=data['username']).first()
            if existe:
                raise ValueError(f"El username '{data['username']}' ya está registrado")
        
        # Validar email único si se está cambiando
        if data.get('email') and data['email'] != empleado.email:
            existe = Empleado.query.filter_by(email=data['email']).first()
            if existe:
                raise ValueError(f"El email {data['email']} ya está registrado")
        
        # Validar rol si se está cambiando
        if data.get('rol') and data['rol'] not in EmpleadoService.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(EmpleadoService.ROLES_VALIDOS)}")
        
        try:
            if 'primer_nombre' in data:
                empleado.primer_nombre = data['primer_nombre']
            if 'segundo_nombre' in data:
                empleado.segundo_nombre = data['segundo_nombre']
            if 'apellido_paterno' in data:
                empleado.apellido_paterno = data['apellido_paterno']
            if 'apellido_materno' in data:
                empleado.apellido_materno = data['apellido_materno']
            if 'username' in data:
                empleado.username = data['username']
            if 'rol' in data:
                empleado.rol = data['rol']
            if 'email' in data:
                empleado.email = data['email']
            if 'activo' in data:
                empleado.activo = data['activo']
            
            # Actualizar password si se proporciona
            if 'password' in data and data['password']:
                if len(data['password']) < 8:
                    raise ValueError("La contraseña debe tener al menos 8 caracteres")
                empleado.set_password(data['password'])
            
            db.session.commit()
            return empleado
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar empleado: {str(e)}")
    
    @staticmethod
    def eliminar(empleado_id):
        """Desactiva un empleado en lugar de eliminarlo físicamente"""
        empleado = EmpleadoService.obtener_por_id(empleado_id)
        
        # Validar que no sea el superusuario
        if empleado.username == 'sa':
            raise ValueError("No se puede desactivar el superusuario del sistema")
        
        # Validar que no tenga ventas asociadas
        if empleado.ventas:
            raise ValueError("No se puede desactivar un empleado con ventas registradas. Considere marcarlo como inactivo.")
        
        try:
            empleado.activo = False
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al desactivar empleado: {str(e)}")
    
    @staticmethod
    def buscar_por_username(username):
        """Busca un empleado por username"""
        return Empleado.query.filter_by(username=username).first()
    
    @staticmethod
    def obtener_por_rol(rol):
        """Obtiene empleados por rol específico"""
        if rol not in EmpleadoService.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(EmpleadoService.ROLES_VALIDOS)}")
        return Empleado.query.filter_by(rol=rol, activo=True).all()
    
    @staticmethod
    def serializar(empleado):
        """Serializa un empleado a diccionario (sin password)"""
        return {
            "id": empleado.id,
            "primer_nombre": empleado.primer_nombre,
            "segundo_nombre": empleado.segundo_nombre,
            "apellido_paterno": empleado.apellido_paterno,
            "apellido_materno": empleado.apellido_materno,
            "username": empleado.username,
            "rol": empleado.rol,
            "email": empleado.email,
            "activo": empleado.activo,
            "created_at": empleado.created_at.isoformat() if empleado.created_at else None
        }