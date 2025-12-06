"""
Script para verificar el rol actual de los usuarios
Ejecutar con: python check_current_roles.py
"""
import sqlite3

def check_roles():
    print("=" * 70)
    print("VERIFICACIÓN DE ROLES ACTUALES")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Obtener todos los usuarios con sus roles
    cursor.execute("""
        SELECT id, username, primer_nombre, apellido_paterno, rol, activo 
        FROM empleado 
        ORDER BY id
    """)
    usuarios = cursor.fetchall()
    
    print("\n📊 Usuarios en la base de datos:\n")
    for user_id, username, nombre, apellido, rol, activo in usuarios:
        estado = "✓ Activo" if activo else "✗ Inactivo"
        print(f"   ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Nombre: {nombre} {apellido}")
        print(f"   Rol: '{rol}'")
        print(f"   Estado: {estado}")
        print("-" * 70)
    
    # Verificar el usuario sa específicamente
    cursor.execute("SELECT rol FROM empleado WHERE username = 'sa'")
    sa_role = cursor.fetchone()
    
    if sa_role:
        print(f"\n🔍 Rol del usuario 'sa': '{sa_role[0]}'")
        
        if sa_role[0] == 'ADMINISTRADOR':
            print("   ✓ El rol es correcto (ADMINISTRADOR)")
        else:
            print(f"   ❌ El rol debe ser 'ADMINISTRADOR', pero es '{sa_role[0]}'")
            print("\n   💡 Solución: Ejecuta python fix_sa_role.py")
    else:
        print("\n   ❌ Usuario 'sa' no encontrado")
    
    conn.close()
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    check_roles()