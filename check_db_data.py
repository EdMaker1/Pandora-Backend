"""
Script para verificar el contenido de la base de datos
Ejecutar con: python check_db_data.py
"""
import sqlite3

def check_data():
    print("=" * 70)
    print("CONTENIDO DE LA BASE DE DATOS")
    print("=" * 70)
    
    conn = sqlite3.connect('instance/Pandora.db')
    cursor = conn.cursor()
    
    # Tablas a verificar
    tables = ['categoria', 'producto', 'cliente', 'empleado', 'venta']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"\n📊 {table.upper()}: {count} registros")
        
        if count > 0 and count <= 5:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = cursor.fetchall()
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            print(f"   Columnas: {', '.join(columns)}")
            for row in rows:
                print(f"   - {row}")
    
    conn.close()
    print("\n" + "=" * 70)

if __name__ == '__main__':
    check_data()