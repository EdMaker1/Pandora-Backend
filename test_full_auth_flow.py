"""
Script para probar el flujo completo de autenticación
Ejecutar con: python test_full_auth_flow.py
"""
from app import create_app
from models import Empleado
import json

app = create_app()

print("=" * 70)
print("PRUEBA COMPLETA DEL FLUJO DE AUTENTICACIÓN")
print("=" * 70)

# Crear un cliente de prueba
with app.test_client() as client:
    
    # 1. Hacer login
    print("\n1️⃣ Intentando hacer login con 'sa' / '12345678'...")
    response = client.post('/api/auth/login',
                          data=json.dumps({'username': 'sa', 'password': '12345678'}),
                          content_type='application/json')
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.get_json()}")
    
    if response.status_code == 200:
        print("   ✓ Login exitoso")
        
        # 2. Verificar la sesión
        print("\n2️⃣ Verificando datos en la sesión...")
        with client.session_transaction() as sess:
            print(f"   user_id: {sess.get('user_id')}")
            print(f"   username: {sess.get('username')}")
            print(f"   rol: '{sess.get('rol')}'")
            print(f"   nombre_completo: {sess.get('nombre_completo')}")
        
        # 3. Intentar acceder a /api/ventas
        print("\n3️⃣ Intentando acceder a /api/ventas...")
        response = client.get('/api/ventas/')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        if response.status_code == 200:
            print("   ✓ Acceso exitoso a ventas")
        elif response.status_code == 403:
            print("   ❌ Acceso denegado (Sin permisos)")
            
            # Verificar el rol en la BD
            with app.app_context():
                empleado = Empleado.query.get(sess.get('user_id'))
                print(f"\n   🔍 Debug - Rol del empleado en BD: '{empleado.rol}'")
                print(f"   🔍 Debug - Roles permitidos: ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO']")
                print(f"   🔍 Debug - ¿Rol está en la lista? {empleado.rol in ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO']}")
        elif response.status_code == 401:
            print("   ❌ No autenticado")
        else:
            print(f"   ❌ Error inesperado")
        
        # 4. Intentar acceder a /api/productos
        print("\n4️⃣ Intentando acceder a /api/productos...")
        response = client.get('/api/productos/')
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Acceso exitoso a productos")
        elif response.status_code == 403:
            print("   ❌ Acceso denegado (Sin permisos)")
        
    else:
        print("   ❌ Login fallido")

print("\n" + "=" * 70)