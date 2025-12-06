"""
Script para verificar qué base de datos está usando Flask
Ejecutar con: python check_db_connection.py
"""
from app import create_app
import os

app = create_app()

print("=" * 70)
print("VERIFICACIÓN DE CONEXIÓN A BASE DE DATOS")
print("=" * 70)

with app.app_context():
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    print(f"\n📋 SQLALCHEMY_DATABASE_URI configurado:")
    print(f"   {db_uri}")
    
    # Extraer la ruta del archivo si es SQLite
    if db_uri and db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        print(f"\n📁 Ruta de la base de datos:")
        print(f"   {db_path}")
        
        # Verificar si el archivo existe
        if os.path.exists(db_path):
            print(f"   ✓ El archivo existe")
            print(f"   Tamaño: {os.path.getsize(db_path)} bytes")
        else:
            print(f"   ❌ El archivo NO existe")
            
        # Verificar si instance/Pandora.db existe
        if os.path.exists('instance/Pandora.db'):
            print(f"\n📁 instance/Pandora.db:")
            print(f"   ✓ Existe")
            print(f"   Tamaño: {os.path.getsize('instance/Pandora.db')} bytes")
            
            if db_path != 'instance/Pandora.db' and not db_path.endswith('instance/Pandora.db'):
                print(f"\n⚠️  ADVERTENCIA: Flask NO está usando instance/Pandora.db")
                print(f"   Flask usa: {db_path}")
                print(f"   Deberías usar: instance/Pandora.db")
        
print("\n" + "=" * 70)
print("\nCONFIGURACIÓN DE config.py:")
print("=" * 70)

if os.path.exists('config.py'):
    with open('config.py', 'r') as f:
        print(f.read())