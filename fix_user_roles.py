"""
Script para corregir roles incorrectos en la base de datos
Ejecutar con: python fix_user_roles.py
"""
import sqlite3

def fix_roles():
    print("=" * 70)
    print("CORRECCIÓN DE ROLES INCORRECTOS")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Mapeo de roles incorrectos a correctos
    role_fixes = {
        'ADMIN': 'ADMINISTRADOR',
        'admin': 'ADMINISTRADOR',
        'administrador': 'ADMINISTRADOR',
        'VENTAS': 'VENDEDOR',
        'ventas': 'VENDEDOR',
        'CAJERA': 'CAJERO',
        'cajera': 'CAJERO',
        'cajero': 'CAJERO',
        'Cajera2': 'CAJERO',
        'ALMACEN': 'ALMACEN',
        'almacen': 'ALMACEN',
        'almacenero': 'ALMACEN',
        'SOPORTE': 'SOPORTE',
        'soporte': 'SOPORTE'
    }
    
    # Obtener todos los usuarios
    cursor.execute("SELECT id, username, rol FROM empleado")
    usuarios = cursor.fetchall()
    
    print("\n🔍 Verificando roles...")
    print("-" * 70)
    
    updates_made = 0
    
    for user_id, username, current_rol in usuarios:
        if current_rol in role_fixes:
            new_rol = role_fixes[current_rol]
            
            if current_rol != new_rol:
                cursor.execute("UPDATE empleado SET rol = ? WHERE id = ?", (new_rol, user_id))
                print(f"   ✓ {username:15} → '{current_rol}' → '{new_rol}'")
                updates_made += 1
            else:
                print(f"   - {username:15} → '{current_rol}' (OK)")
        else:
            # Rol desconocido
            print(f"   ⚠️  {username:15} → '{current_rol}' (ROL DESCONOCIDO)")
    
    if updates_made > 0:
        conn.commit()
        print(f"\n✓ Se actualizaron {updates_made} usuario(s)")
    else:
        print("\n- No se necesitaron cambios")
    
    # Mostrar resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE ROLES:")
    print("=" * 70)
    
    cursor.execute("SELECT rol, COUNT(*) FROM empleado GROUP BY rol ORDER BY rol")
    role_counts = cursor.fetchall()
    
    for rol, count in role_counts:
        print(f"   {rol:20} → {count} usuario(s)")
    
    # Mostrar todos los usuarios
    print("\n" + "=" * 70)
    print("USUARIOS ACTUALIZADOS:")
    print("=" * 70)
    
    cursor.execute("""
        SELECT username, primer_nombre, apellido_paterno, rol, activo 
        FROM empleado 
        ORDER BY id
    """)
    
    usuarios = cursor.fetchall()
    for username, nombre, apellido, rol, activo in usuarios:
        estado = "✓ Activo" if activo else "✗ Inactivo"
        print(f"   {username:15} ({nombre} {apellido:20}) → {rol:15} | {estado}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ CORRECCIÓN COMPLETADA")
    print("=" * 70)
    print("""
Siguiente paso:
   1. Cierra sesión del usuario 'lmango' en el navegador
   2. Limpia localStorage: localStorage.clear() en la consola
   3. Vuelve a iniciar sesión con 'lmango'
   4. Ahora debería tener permisos completos
""")

if __name__ == '__main__':
    fix_roles()