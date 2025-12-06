"""
Script para crear o actualizar el superusuario 'sa'
Ejecutar con: python create_superuser.py
"""
from app import create_app
from models import db, Empleado

def create_super_user():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("  CREACIÓN/ACTUALIZACIÓN DE SUPERUSUARIO")
        print("=" * 60)
        
        # Verificar si ya existe
        existing = Empleado.query.filter_by(username='sa').first()
        
        if existing:
            print("\n⚠️  El usuario 'sa' ya existe en el sistema")
            print(f"   ID: {existing.id}")
            print(f"   Nombre: {existing.primer_nombre} {existing.apellido_paterno}")
            print(f"   Rol: {existing.rol}")
            print(f"   Email: {existing.email}")
            print(f"   Activo: {'Sí' if existing.activo else 'No'}")
            
            # Preguntar si desea actualizar
            print("\n¿Qué deseas hacer?")
            print("1. Actualizar contraseña")
            print("2. Activar/Desactivar usuario")
            print("3. Cancelar")
            
            opcion = input("\nSelecciona una opción (1-3): ").strip()
            
            if opcion == '1':
                existing.set_password('12345678.')
                db.session.commit()
                print("\n✅ Contraseña actualizada a: 12345678.")
                
            elif opcion == '2':
                existing.activo = not existing.activo
                db.session.commit()
                estado = "activado" if existing.activo else "desactivado"
                print(f"\n✅ Usuario {estado}")
                
            else:
                print("\n❌ Operación cancelada")
        else:
            # Crear nuevo superusuario
            print("\n📝 Creando nuevo superusuario...")
            
            superuser = Empleado(
                primer_nombre='Super',
                segundo_nombre='Admin',
                apellido_paterno='System',
                apellido_materno='Admin',
                username='sa',
                rol='ADMIN',
                email='admin@pandora.com',
                activo=True
            )
            superuser.set_password('12345678.')
            
            db.session.add(superuser)
            db.session.commit()
            
            print("\n✅ ¡Superusuario creado exitosamente!")
            print("\n" + "=" * 60)
            print("  CREDENCIALES DE ACCESO")
            print("=" * 60)
            print(f"  Username: sa")
            print(f"  Password: 12345678.")
            print(f"  Rol:      ADMIN (acceso completo)")
            print(f"  ID:       {superuser.id}")
            print("=" * 60)
            print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
        print("\n✨ Proceso completado\n")

if __name__ == '__main__':
    create_super_user()