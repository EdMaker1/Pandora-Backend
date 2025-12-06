"""
Script para probar la autenticación y verificar el decorador role_required
Ejecutar con: python test_role_decorator.py
"""
from app import create_app
from models import db, Empleado
from flask import session

app = create_app()

def test_role_verification():
    print("=" * 70)
    print("PRUEBA DE VERIFICACIÓN DE ROLES")
    print("=" * 70)
    
    with app.app_context():
        # Verificar usuario sa
        print("\n🔍 Verificando usuario 'sa':")
        print("-" * 70)
        
        sa_user = Empleado.query.filter_by(username='sa').first()
        
        if sa_user:
            print(f"✓ Usuario encontrado")
            print(f"   ID: {sa_user.id}")
            print(f"   Username: {sa_user.username}")
            print(f"   Rol: '{sa_user.rol}'")
            print(f"   Tipo de dato: {type(sa_user.rol)}")
            print(f"   Activo: {sa_user.activo}")
            
            # Verificar si el rol está en la lista de roles permitidos
            roles_permitidos = ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO']
            
            print(f"\n   Roles permitidos para Ventas: {roles_permitidos}")
            print(f"   ¿'{sa_user.rol}' está en la lista? {sa_user.rol in roles_permitidos}")
            
            # Verificar con comparación explícita
            for rol in roles_permitidos:
                print(f"   ¿'{sa_user.rol}' == '{rol}'? {sa_user.rol == rol}")
        else:
            print("❌ Usuario 'sa' no encontrado")
        
        # Verificar todos los usuarios
        print("\n" + "=" * 70)
        print("📊 TODOS LOS USUARIOS Y SUS ROLES:")
        print("=" * 70)
        
        usuarios = Empleado.query.all()
        for user in usuarios:
            print(f"\nUsuario: {user.username}")
            print(f"   Rol: '{user.rol}'")
            print(f"   Rol (repr): {repr(user.rol)}")
            print(f"   Rol (bytes): {user.rol.encode('utf-8')}")
            print(f"   Longitud: {len(user.rol)}")

if __name__ == '__main__':
    test_role_verification()