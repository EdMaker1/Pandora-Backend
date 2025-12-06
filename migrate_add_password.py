"""
Script para migrar la base de datos agregando la columna password_hash
Ejecutar con: python migrate_add_password.py
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

def migrate_database():
    """Agrega la columna password_hash a la tabla empleado"""
    
    db_path = 'instance/Pandora.db'
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en: {db_path}")
        return
    
    print("=" * 70)
    print("MIGRACIÓN DE BASE DE DATOS - Agregar password_hash")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna password_hash ya existe
        cursor.execute("PRAGMA table_info(empleado);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'password_hash' in column_names:
            print("\n✓ La columna 'password_hash' ya existe en la tabla empleado")
        else:
            print("\n🔧 Agregando columna 'password_hash' a la tabla empleado...")
            cursor.execute("ALTER TABLE empleado ADD COLUMN password_hash VARCHAR(255);")
            conn.commit()
            print("✓ Columna 'password_hash' agregada exitosamente")
        
        # Verificar usuarios actuales
        print("\n📊 Usuarios actuales en la base de datos:")
        cursor.execute("SELECT id, username, primer_nombre, apellido_paterno, activo FROM empleado;")
        usuarios = cursor.fetchall()
        
        for user in usuarios:
            user_id, username, nombre, apellido, activo = user
            estado = "Activo" if activo else "Inactivo"
            print(f"   - ID: {user_id} | Username: {username} | Nombre: {nombre} {apellido} | Estado: {estado}")
        
        # Verificar si existe el usuario 'sa'
        cursor.execute("SELECT id FROM empleado WHERE username = 'sa';")
        sa_user = cursor.fetchone()
        
        if sa_user:
            print("\n✓ El usuario 'sa' ya existe (ID: {})".format(sa_user[0]))
            
            # Actualizar contraseña del usuario 'sa'
            print("🔧 Actualizando contraseña del usuario 'sa'...")
            password_hash = generate_password_hash('12345678')
            cursor.execute("UPDATE empleado SET password_hash = ? WHERE username = 'sa';", (password_hash,))
            conn.commit()
            print("✓ Contraseña actualizada para el usuario 'sa'")
            
        else:
            print("\n⚠ El usuario 'sa' no existe. Creándolo...")
            
            # Crear usuario administrador 'sa'
            password_hash = generate_password_hash('12345678')
            
            cursor.execute("""
                INSERT INTO empleado 
                (primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, 
                 username, password_hash, rol, email, activo, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                'Super',
                'Admin',
                'Administrador',
                'Sistema',
                'sa',
                password_hash,
                'administrador',
                'admin@pandora.com',
                1  # activo = True
            ))
            
            conn.commit()
            print("✓ Usuario 'sa' creado exitosamente")
            print("   - Username: sa")
            print("   - Password: 12345678")
            print("   - Rol: administrador")
        
        # Actualizar contraseñas de usuarios existentes (opcional)
        print("\n🔧 Actualizando contraseñas de usuarios existentes...")
        
        # Password por defecto para usuarios sin contraseña
        default_password = generate_password_hash('password123')
        
        cursor.execute("UPDATE empleado SET password_hash = ? WHERE password_hash IS NULL;", (default_password,))
        rows_updated = cursor.rowcount
        conn.commit()
        
        if rows_updated > 0:
            print(f"✓ Se actualizaron {rows_updated} usuarios con contraseña por defecto: 'password123'")
            print("   ⚠ IMPORTANTE: Los usuarios deben cambiar esta contraseña")
        else:
            print("✓ Todos los usuarios ya tienen contraseña configurada")
        
        # Mostrar resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN FINAL")
        print("=" * 70)
        
        cursor.execute("SELECT COUNT(*) FROM empleado;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empleado WHERE activo = 1;")
        activos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empleado WHERE password_hash IS NOT NULL;")
        con_password = cursor.fetchone()[0]
        
        print(f"Total de empleados: {total}")
        print(f"Empleados activos: {activos}")
        print(f"Empleados con contraseña: {con_password}")
        
        print("\n✓ Migración completada exitosamente")
        print("=" * 70)
        
    except sqlite3.Error as e:
        print(f"\n❌ Error durante la migración: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()