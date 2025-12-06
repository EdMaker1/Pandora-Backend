"""
Script para inicializar la base de datos
Ejecutar con: python init_db.py
"""
from app import app, db
from models.empleado import Empleado
from werkzeug.security import generate_password_hash

def init_database():
    """Crea todas las tablas y un usuario administrador inicial"""
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("✓ Tablas creadas exitosamente")
        
        # Verificar si ya existe el usuario 'sa'
        existing_user = Empleado.query.filter_by(username='sa').first()
        
        if not existing_user:
            # Crear usuario administrador
            print("\nCreando usuario administrador 'sa'...")
            admin = Empleado(
                primer_nombre='Super',
                apellido_paterno='Administrador',
                username='sa',
                password_hash=generate_password_hash('12345678'),
                rol='administrador',
                email='admin@pandora.com',
                activo=True
            )
            
            db.session.add(admin)
            db.session.commit()
            print("✓ Usuario administrador creado exitosamente")
            print(f"  Username: sa")
            print(f"  Password: 12345678")
        else:
            print("\n⚠ El usuario 'sa' ya existe en la base de datos")
        
        print("\n✓ Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_database()