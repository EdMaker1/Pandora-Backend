"""
Script para corregir el rol del usuario sa y otros usuarios
Ejecutar con: python fix_sa_role.py
"""
import sqlite3

def fix_user_roles():
    print("=" * 70)
    print("CORRECCIÓN DE ROLES")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Verificar roles actuales
    print("\n📊 Roles actuales:")
    cursor.execute("SELECT id, username, rol FROM empleado ORDER BY id")
    usuarios = cursor.fetchall()
    
    for user_id, username, rol in usuarios:
        print(f"   {username}: '{rol}'")
    
    print("\n🔧 Corrigiendo roles...")
    print("-" * 70)
    
    # Actualizar usuario 'sa' a ADMINISTRADOR
    cursor.execute("UPDATE empleado SET rol = 'ADMINISTRADOR' WHERE username = 'sa'")
    if cursor.rowcount > 0:
        print("   ✓ Usuario 'sa' actualizado a 'ADMINISTRADOR'")
    
    # Actualizar otros usuarios según sea necesario
    # Cambiar 'administrador' a 'ADMINISTRADOR'
    cursor.execute("UPDATE empleado SET rol = 'ADMINISTRADOR' WHERE rol = 'administrador'")
    if cursor.rowcount > 0:
        print(f"   ✓ {cursor.rowcount} usuario(s) actualizado(s): 'administrador' → 'ADMINISTRADOR'")
    
    # Cambiar variantes de cajero
    cursor.execute("UPDATE empleado SET rol = 'CAJERO' WHERE rol IN ('cajero', 'Cajera', 'Cajera2', 'cajera')")
    if cursor.rowcount > 0:
        print(f"   ✓ {cursor.rowcount} usuario(s) actualizado(s) a 'CAJERO'")
    
    # Cambiar variantes de vendedor
    cursor.execute("UPDATE empleado SET rol = 'VENDEDOR' WHERE rol IN ('vendedor', 'Vendedor')")
    if cursor.rowcount > 0:
        print(f"   ✓ {cursor.rowcount} usuario(s) actualizado(s) a 'VENDEDOR'")
    
    # Cambiar variantes de almacen
    cursor.execute("UPDATE empleado SET rol = 'ALMACEN' WHERE rol IN ('almacen', 'Almacen', 'almacenero', 'Almacenero')")
    if cursor.rowcount > 0:
        print(f"   ✓ {cursor.rowcount} usuario(s) actualizado(s) a 'ALMACEN'")
    
    # Cambiar variantes de soporte
    cursor.execute("UPDATE empleado SET rol = 'SOPORTE' WHERE rol IN ('soporte', 'Soporte')")
    if cursor.rowcount > 0:
        print(f"   ✓ {cursor.rowcount} usuario(s) actualizado(s) a 'SOPORTE'")
    
    conn.commit()
    
    # Mostrar roles actualizados
    print("\n" + "=" * 70)
    print("📊 ROLES ACTUALIZADOS:")
    print("=" * 70)
    
    cursor.execute("SELECT id, username, primer_nombre, apellido_paterno, rol, activo FROM empleado ORDER BY id")
    usuarios = cursor.fetchall()
    
    for user_id, username, nombre, apellido, rol, activo in usuarios:
        estado = "✓" if activo else "✗"
        print(f"\n   {user_id}. {username} ({nombre} {apellido})")
        print(f"      Rol: {rol}")
        print(f"      Activo: {estado}")
    
    # Resumen de roles
    cursor.execute("SELECT rol, COUNT(*) FROM empleado GROUP BY rol ORDER BY rol")
    rol_counts = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE ROLES:")
    print("=" * 70)
    for rol, count in rol_counts:
        print(f"   {rol}: {count} usuario(s)")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ CORRECCIÓN COMPLETADA")
    print("=" * 70)
    print("""
Siguiente paso:
   1. Cierra sesión en el navegador
   2. Reinicia el servidor Flask: python app.py
   3. Vuelve a iniciar sesión con 'sa' / '12345678'
   4. Ahora deberías tener acceso completo a todos los módulos
""")

if __name__ == '__main__':
    fix_user_roles()