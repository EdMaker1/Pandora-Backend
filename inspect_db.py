"""
Script para inspeccionar la base de datos Pandora.db
Ejecutar con: python inspect_db.py
"""
import sqlite3
import os

def inspect_database():
    """Inspecciona el contenido de la base de datos"""
    
    # Buscar el archivo de base de datos
    db_paths = [
        'instance/Pandora.db',
        'Pandora.db',
        'instance/pandora.db',
        'pandora.db'
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ No se encontró el archivo de base de datos Pandora.db")
        print("\nBuscado en:")
        for path in db_paths:
            print(f"  - {path}")
        return
    
    print(f"✓ Base de datos encontrada en: {db_path}\n")
    print("=" * 70)
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📋 TABLAS EN LA BASE DE DATOS:")
    print("=" * 70)
    
    if not tables:
        print("⚠ No hay tablas en la base de datos")
    else:
        for table in tables:
            table_name = table[0]
            print(f"\n🔹 Tabla: {table_name}")
            
            # Obtener estructura de la tabla
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"   Columnas:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_str = " [PRIMARY KEY]" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                print(f"     - {col_name}: {col_type}{not_null_str}{pk_str}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   Registros: {count}")
            
            # Si es la tabla de empleados/usuarios, mostrar los usuarios
            if table_name.lower() in ['empleado', 'usuario', 'user', 'empleados', 'users']:
                print(f"\n   📊 Contenido de {table_name}:")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
                rows = cursor.fetchall()
                
                if rows:
                    # Obtener nombres de columnas
                    col_names = [description[0] for description in cursor.description]
                    print(f"      {' | '.join(col_names)}")
                    print("      " + "-" * 60)
                    
                    for row in rows:
                        # Truncar valores largos para mejor visualización
                        display_row = []
                        for val in row:
                            if isinstance(val, str) and len(val) > 30:
                                display_row.append(val[:27] + "...")
                            else:
                                display_row.append(str(val))
                        print(f"      {' | '.join(display_row)}")
                else:
                    print("      (vacía)")
    
    print("\n" + "=" * 70)
    print("\n✓ Inspección completada")
    
    conn.close()

if __name__ == '__main__':
    inspect_database()