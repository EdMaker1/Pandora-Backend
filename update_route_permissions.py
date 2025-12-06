"""
Script para actualizar los decoradores @role_required en las rutas
Ejecutar con: python update_route_permissions.py
"""
import os
import re

# Definir los permisos por módulo según los requisitos
PERMISSIONS = {
    'ventas': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO'],
    'productos': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN'],
    'categorias': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN'],
    'clientes': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO'],
    'reportes': ['ADMINISTRADOR', 'SOPORTE', 'CAJERO'],
    'stock_adjustment': ['ADMINISTRADOR', 'SOPORTE', 'ALMACEN'],
    'empleados': ['ADMINISTRADOR', 'SOPORTE'],  # Solo admin y soporte
    'pagos': ['ADMINISTRADOR', 'SOPORTE', 'CAJERO'],  # Pagos para admin, soporte y cajero
}

def update_route_file(filename, module_name):
    """Actualiza los decoradores @role_required en un archivo de ruta"""
    
    filepath = os.path.join('routes', filename)
    
    if not os.path.exists(filepath):
        return False
    
    print(f"\n📝 Procesando: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Obtener roles permitidos para este módulo
    allowed_roles = PERMISSIONS.get(module_name, ['ADMINISTRADOR', 'SOPORTE'])
    roles_str = ', '.join([f"'{role}'" for role in allowed_roles])
    
    # Reemplazar todos los decoradores @role_required
    # Patrón para encontrar: @role_required('ADMIN', 'SOPORTE', ...)
    pattern = r"@role_required\([^)]+\)"
    replacement = f"@role_required({roles_str})"
    
    content = re.sub(pattern, replacement, content)
    
    # Verificar si hubo cambios
    if content != original_content:
        # Hacer backup
        backup_path = filepath + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Escribir el archivo actualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✓ Actualizado → @role_required({roles_str})")
        print(f"   ✓ Backup guardado: {filename}.backup")
        return True
    else:
        print(f"   - Sin cambios necesarios")
        return False

def main():
    print("=" * 70)
    print("ACTUALIZACIÓN DE PERMISOS EN RUTAS")
    print("=" * 70)
    
    print("\n📋 Configuración de permisos:")
    print("-" * 70)
    for module, roles in PERMISSIONS.items():
        roles_display = ', '.join(roles)
        print(f"   {module:20} → {roles_display}")
    
    print("\n" + "=" * 70)
    print("🔧 Actualizando archivos de rutas...")
    print("=" * 70)
    
    # Mapeo de archivos a módulos
    route_files = {
        'ventas.py': 'ventas',
        'productos.py': 'productos',
        'categorias.py': 'categorias',
        'clientes.py': 'clientes',
        'reportes.py': 'reportes',
        'stock_adjustment.py': 'stock_adjustment',
        'empleados.py': 'empleados',
        'pagos.py': 'pagos',
    }
    
    updated_count = 0
    
    for filename, module_name in route_files.items():
        if update_route_file(filename, module_name):
            updated_count += 1
    
    print("\n" + "=" * 70)
    print("✓ ACTUALIZACIÓN COMPLETADA")
    print("=" * 70)
    print(f"\n   Archivos actualizados: {updated_count}")
    print(f"   Total procesados: {len(route_files)}")
    
    print("\n📋 RESUMEN DE PERMISOS POR ROL:")
    print("=" * 70)
    
    # Crear resumen invertido (por rol, qué puede hacer)
    role_permissions = {}
    for module, roles in PERMISSIONS.items():
        for role in roles:
            if role not in role_permissions:
                role_permissions[role] = []
            role_permissions[role].append(module)
    
    for role in sorted(role_permissions.keys()):
        print(f"\n📌 {role}:")
        modules = sorted(role_permissions[role])
        for module in modules:
            print(f"   ✓ {module}")
    
    print("\n" + "=" * 70)
    print("Siguiente paso:")
    print("   1. Revisar los archivos modificados (los backups están en routes/*.backup)")
    print("   2. Reiniciar el servidor: python app.py")
    print("   3. Probar el acceso con diferentes roles")
    print("=" * 70)

if __name__ == '__main__':
    main()