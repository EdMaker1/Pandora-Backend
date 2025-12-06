"""
Script para actualizar los roles en la base de datos
Ejecutar con: python update_roles.py
"""
import sqlite3

def update_roles():
    print("=" * 70)
    print("ACTUALIZACIÓN DE ROLES EN BASE DE DATOS")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Mostrar usuarios actuales
    print("\n📊 Usuarios actuales:")
    cursor.execute("SELECT id, username, primer_nombre, apellido_paterno, rol FROM empleado;")
    usuarios = cursor.fetchall()
    
    for user_id, username, nombre, apellido, rol in usuarios:
        print(f"   {user_id}. {username} ({nombre} {apellido}) - Rol actual: '{rol}'")
    
    # Mapeo de roles antiguos a nuevos roles estándar
    role_mapping = {
        'administrador': 'ADMINISTRADOR',
        'admin': 'ADMINISTRADOR',
        'ADMIN': 'ADMINISTRADOR',
        'Cajera2': 'CAJERO',
        'cajera': 'CAJERO',
        'cajero': 'CAJERO',
        'vendedor': 'VENDEDOR',
        'soporte': 'SOPORTE',
        'SOPORTE': 'SOPORTE',
        'almacen': 'ALMACEN',
        'ALMACEN': 'ALMACEN',
        'almacenero': 'ALMACEN'
    }
    
    print("\n🔧 Actualizando roles...")
    print("-" * 70)
    
    updates_made = 0
    
    for user_id, username, nombre, apellido, old_rol in usuarios:
        new_rol = role_mapping.get(old_rol, old_rol.upper())
        
        if old_rol != new_rol:
            cursor.execute("UPDATE empleado SET rol = ? WHERE id = ?;", (new_rol, user_id))
            print(f"   ✓ {username}: '{old_rol}' → '{new_rol}'")
            updates_made += 1
        else:
            print(f"   - {username}: '{old_rol}' (sin cambios)")
    
    if updates_made > 0:
        conn.commit()
        print(f"\n✓ Se actualizaron {updates_made} usuarios")
    else:
        print("\n- No se realizaron cambios")
    
    # Mostrar usuarios actualizados
    print("\n" + "=" * 70)
    print("📊 USUARIOS ACTUALIZADOS:")
    print("=" * 70)
    
    cursor.execute("SELECT id, username, primer_nombre, apellido_paterno, rol, activo FROM empleado ORDER BY id;")
    usuarios = cursor.fetchall()
    
    for user_id, username, nombre, apellido, rol, activo in usuarios:
        estado = "✓ Activo" if activo else "✗ Inactivo"
        print(f"\n   {user_id}. {username} ({nombre} {apellido})")
        print(f"      Rol: {rol}")
        print(f"      Estado: {estado}")
    
    # Resumen de roles
    cursor.execute("SELECT DISTINCT rol FROM empleado ORDER BY rol;")
    roles = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print("📋 ROLES EN EL SISTEMA:")
    print("=" * 70)
    for rol in roles:
        print(f"   - {rol[0]}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ ACTUALIZACIÓN COMPLETADA")
    print("=" * 70)
    print("""
PERMISOS POR ROL:

📌 ADMINISTRADOR:
   ✓ Sin restricciones (acceso a todo)

📌 SOPORTE:
   ✓ Sin restricciones (acceso a todo)

📌 VENDEDOR:
   ✓ Ventas (lectura y escritura)
   ✓ Productos (lectura y escritura)
   ✓ Categorías (lectura y escritura)
   ✓ Clientes (lectura y escritura)

📌 CAJERO:
   ✓ Ventas (lectura y escritura)
   ✓ Productos (lectura y escritura)
   ✓ Categorías (lectura y escritura)
   ✓ Clientes (lectura y escritura)
   ✓ Reportes (lectura y escritura)

📌 ALMACEN:
   ✓ Stock Adjustments (lectura y escritura)
   ✓ Productos (lectura y escritura)
   ✓ Categorías (lectura y escritura)

Siguiente paso:
   → Ejecutar: python update_route_permissions.py
   → Esto actualizará los decoradores en las rutas
""")

if __name__ == '__main__':
    update_roles()