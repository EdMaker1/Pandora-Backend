"""
Script para verificar el usuario lmango
Ejecutar con: python check_lmango.py
"""
import sqlite3

def check_user():
    print("=" * 70)
    print("VERIFICACIÓN DEL USUARIO lmango")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Buscar usuario lmango
    cursor.execute("""
        SELECT id, username, primer_nombre, apellido_paterno, rol, activo, email
        FROM empleado 
        WHERE username = 'lmango'
    """)
    
    user = cursor.fetchone()
    
    if user:
        user_id, username, nombre, apellido, rol, activo, email = user
        print(f"\n✓ Usuario encontrado:")
        print(f"   ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Nombre: {nombre} {apellido}")
        print(f"   Rol: '{rol}'")
        print(f"   Rol (repr): {repr(rol)}")
        print(f"   Rol (bytes): {rol.encode('utf-8')}")
        print(f"   Email: {email}")
        print(f"   Activo: {activo}")
        
        # Verificar si el rol es correcto
        if rol == 'ADMINISTRADOR':
            print("\n   ✓ El rol en BD es correcto: 'ADMINISTRADOR'")
        elif rol == 'ADMIN':
            print("\n   ⚠️  El rol en BD es 'ADMIN' (debería ser 'ADMINISTRADOR')")
            print("   💡 Solución: Actualizar el rol a 'ADMINISTRADOR'")
        else:
            print(f"\n   ❌ El rol '{rol}' no es reconocido")
    else:
        print("\n❌ Usuario 'lmango' no encontrado")
    
    # Mostrar todos los usuarios
    print("\n" + "=" * 70)
    print("TODOS LOS USUARIOS:")
    print("=" * 70)
    
    cursor.execute("""
        SELECT username, rol, activo 
        FROM empleado 
        ORDER BY id
    """)
    
    users = cursor.fetchall()
    for username, rol, activo in users:
        estado = "✓" if activo else "✗"
        print(f"   {estado} {username:15} → {rol}")
    
    conn.close()
    print("\n" + "=" * 70)

if __name__ == '__main__':
    check_user()