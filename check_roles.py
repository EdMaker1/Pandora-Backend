"""
Script para verificar la configuración de roles en las rutas
Ejecutar con: python check_roles.py
"""
import os
import glob
import re

print("=" * 70)
print("VERIFICACIÓN DE ROLES EN LAS RUTAS")
print("=" * 70)

# Buscar todos los archivos de rutas
route_files = glob.glob('routes/*.py')

roles_found = set()
role_patterns = []

print("\n🔍 Analizando archivos de rutas...")
print("-" * 70)

for route_file in sorted(route_files):
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Buscar decoradores @role_required
        matches = re.findall(r"@role_required\((.*?)\)", content)
        
        if matches:
            print(f"\n📄 {route_file}:")
            for match in matches:
                # Extraer los roles
                roles = re.findall(r"['\"](\w+)['\"]", match)
                for rol in roles:
                    roles_found.add(rol)
                print(f"   @role_required({match})")
                role_patterns.append((route_file, match))

print("\n" + "=" * 70)
print("📊 ROLES ENCONTRADOS EN LAS RUTAS:")
print("=" * 70)
for rol in sorted(roles_found):
    print(f"   - {rol}")

# Verificar roles en la base de datos
print("\n" + "=" * 70)
print("📊 ROLES EN LA BASE DE DATOS:")
print("=" * 70)

import sqlite3
conn = sqlite3.connect('instance/Pandora.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT rol FROM empleado;")
db_roles = cursor.fetchall()

print("\nRoles actuales en la tabla empleado:")
for rol in db_roles:
    print(f"   - {rol[0]}")

cursor.execute("SELECT id, username, rol FROM empleado;")
usuarios = cursor.fetchall()

print("\nUsuarios y sus roles:")
for user_id, username, rol in usuarios:
    print(f"   - {username}: '{rol}'")

conn.close()

# Análisis
print("\n" + "=" * 70)
print("⚠️  ANÁLISIS:")
print("=" * 70)

print("\nROLES ESPERADOS POR LAS RUTAS vs ROLES EN BD:")
for rol in sorted(roles_found):
    db_rol_list = [r[0] for r in db_roles]
    if rol in db_rol_list:
        print(f"   ✓ '{rol}' - COINCIDE")
    else:
        print(f"   ❌ '{rol}' - NO EXISTE EN BD")
        # Buscar similar
        similar = [r for r in db_rol_list if r.upper() == rol.upper()]
        if similar:
            print(f"      Encontrado similar: '{similar[0]}'")

print("\n" + "=" * 70)
print("RECOMENDACIÓN:")
print("=" * 70)
print("""
Si los roles no coinciden, tienes dos opciones:

OPCIÓN 1: Actualizar los roles en la base de datos (RECOMENDADO)
   - Cambiar 'administrador' a 'ADMIN'
   - Cambiar 'Cajera2' a un rol estándar como 'CAJERO' o 'VENDEDOR'

OPCIÓN 2: Modificar los decoradores en las rutas
   - Cambiar @role_required('ADMIN') a @role_required('administrador')
   - Ajustar todos los decoradores para que coincidan con la BD
""")