"""
Capa lógica para gestión de categorías
"""
from models import db, Categoria
from sqlalchemy.exc import SQLAlchemyError

class CategoriaService:
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las categorías"""
        try:
            return Categoria.query.all()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")
    
    @staticmethod
    def obtener_por_id(categoria_id):
        """Obtiene una categoría por su ID"""
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            raise ValueError(f"Categoría con ID {categoria_id} no encontrada")
        return categoria
    
    @staticmethod
    def crear(data):
        """
        Crea una nueva categoría
        :param data: dict con nombre y descripcion
        :return: Categoria creada
        """
        if not data.get('nombre'):
            raise ValueError("El campo 'nombre' es obligatorio")
        
        # Validar nombre único
        existe = Categoria.query.filter_by(nombre=data['nombre']).first()
        if existe:
            raise ValueError(f"La categoría '{data['nombre']}' ya existe")
        
        try:
            categoria = Categoria(
                nombre=data['nombre'],
                descripcion=data.get('descripcion')
            )
            db.session.add(categoria)
            db.session.commit()
            return categoria
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al crear categoría: {str(e)}")
    
    @staticmethod
    def actualizar(categoria_id, data):
        """Actualiza una categoría existente"""
        categoria = CategoriaService.obtener_por_id(categoria_id)
        
        # Validar nombre único si se está cambiando
        if data.get('nombre') and data['nombre'] != categoria.nombre:
            existe = Categoria.query.filter_by(nombre=data['nombre']).first()
            if existe:
                raise ValueError(f"La categoría '{data['nombre']}' ya existe")
        
        try:
            if 'nombre' in data:
                categoria.nombre = data['nombre']
            if 'descripcion' in data:
                categoria.descripcion = data['descripcion']
            
            db.session.commit()
            return categoria
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar categoría: {str(e)}")
    
    @staticmethod
    def eliminar(categoria_id):
        """
        Elimina una categoría (validando que no tenga productos)
        """
        categoria = CategoriaService.obtener_por_id(categoria_id)
        
        # Validar que no tenga productos asociados
        if categoria.productos:
            raise ValueError(
                f"No se puede eliminar la categoría porque tiene {len(categoria.productos)} productos asociados"
            )
        
        try:
            db.session.delete(categoria)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar categoría: {str(e)}")
    
    @staticmethod
    def contar_productos(categoria_id):
        """Cuenta cuántos productos tiene una categoría"""
        categoria = CategoriaService.obtener_por_id(categoria_id)
        return len(categoria.productos)