"""
Script para agregar columnas de Google OAuth a la tabla empleado
Ejecutar con: python add_google_auth.py
"""
import sqlite3

def add_google_columns():
    print("=" * 70)
    print("AGREGANDO SOPORTE DE GOOGLE OAUTH")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    try:
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(empleado)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Agregar columnas SIN constraint UNIQUE
        if 'google_id' not in columns:
            print("\n✓ Agregando columna 'google_id'...")
            cursor.execute("ALTER TABLE empleado ADD COLUMN google_id VARCHAR(255)")
            print("  → Columna 'google_id' agregada")
        else:
            print("\n- Columna 'google_id' ya existe")
        
        if 'google_email' not in columns:
            print("✓ Agregando columna 'google_email'...")
            cursor.execute("ALTER TABLE empleado ADD COLUMN google_email VARCHAR(255)")
            print("  → Columna 'google_email' agregada")
        else:
            print("- Columna 'google_email' ya existe")
        
        if 'google_picture' not in columns:
            print("✓ Agregando columna 'google_picture'...")
            cursor.execute("ALTER TABLE empleado ADD COLUMN google_picture VARCHAR(512)")
            print("  → Columna 'google_picture' agregada")
        else:
            print("- Columna 'google_picture' ya existe")
        
        conn.commit()
        print("\n" + "=" * 70)
        print("✓ ACTUALIZACIÓN COMPLETADA")
        print("=" * 70)
        print("""
Las columnas se agregaron sin constraint UNIQUE debido a limitaciones de SQLite.
La unicidad se manejará a nivel de aplicación en models.py.

Siguiente paso:
   1. Reemplaza models.py con la versión actualizada
   2. Reemplaza routes/auth_google.py con la versión mejorada
   3. Reinicia el servidor Flask
""")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_google_columns()