"""
Script para simular un login y ver qué se guarda en la sesión
Ejecutar con: python test_login_session.py
"""
from app import create_app
from models import Empleado

app = create_app()

print("=" * 70)
print("SIMULACIÓN DE LOGIN")
print("=" * 70)

with app.test_request_context():
    from flask import session
    
    # Simular el login del usuario sa
    empleado = Empleado.query.filter_by(username='sa', activo=True).first()
    
    if empleado:
        print(f"\n✓ Usuario encontrado: {empleado.username}")
        print(f"   Rol en BD: '{empleado.rol}'")
        
        # Simular lo que hace el endpoint de login
        session['user_id'] = empleado.id
        session['username'] = empleado.username
        session['rol'] = empleado.rol
        session['nombre_completo'] = f"{empleado.primer_nombre} {empleado.apellido_paterno}"
        
        print(f"\n📊 Datos guardados en la sesión:")
        print(f"   session['user_id'] = {session.get('user_id')}")
        print(f"   session['username'] = {session.get('username')}")
        print(f"   session['rol'] = '{session.get('rol')}'")
        print(f"   session['nombre_completo'] = {session.get('nombre_completo')}")
        
        # Verificar el tipo de dato
        rol_sesion = session.get('rol')
        print(f"\n🔍 Verificación del rol en sesión:")
        print(f"   Valor: '{rol_sesion}'")
        print(f"   Tipo: {type(rol_sesion)}")
        print(f"   ¿Es 'ADMINISTRADOR'? {rol_sesion == 'ADMINISTRADOR'}")
        print(f"   ¿Está en ['ADMINISTRADOR', 'SOPORTE']? {rol_sesion in ['ADMINISTRADOR', 'SOPORTE']}")
    else:
        print("\n❌ Usuario no encontrado")

print("\n" + "=" * 70)