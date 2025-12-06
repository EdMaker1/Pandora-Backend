"""
Script para visualizar la matriz de permisos
Ejecutar con: python show_permissions_matrix.py
"""

# Definición de permisos
PERMISSIONS = {
    'ventas': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO'],
    'productos': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN'],
    'categorias': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN'],
    'clientes': ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO'],
    'reportes': ['ADMINISTRADOR', 'SOPORTE', 'CAJERO'],
    'stock_adjustment': ['ADMINISTRADOR', 'SOPORTE', 'ALMACEN'],
    'empleados': ['ADMINISTRADOR', 'SOPORTE'],
    'pagos': ['ADMINISTRADOR', 'SOPORTE', 'CAJERO'],
}

def show_matrix():
    print("=" * 90)
    print("MATRIZ DE PERMISOS DEL SISTEMA")
    print("=" * 90)
    
    # Todos los roles
    all_roles = ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN']
    
    # Crear encabezado
    header = f"{'Módulo':<20}"
    for role in all_roles:
        header += f" {role[:5]:>6}"
    
    print("\n" + header)
    print("-" * 90)
    
    # Mostrar cada módulo
    for module in sorted(PERMISSIONS.keys()):
        row = f"{module:<20}"
        allowed_roles = PERMISSIONS[module]
        
        for role in all_roles:
            if role in allowed_roles:
                row += "    ✓ "
            else:
                row += "    ✗ "
        
        print(row)
    
    print("\n" + "=" * 90)
    print("DESCRIPCIÓN DETALLADA POR ROL:")
    print("=" * 90)
    
    # Crear resumen por rol
    role_permissions = {}
    for module, roles in PERMISSIONS.items():
        for role in roles:
            if role not in role_permissions:
                role_permissions[role] = []
            role_permissions[role].append(module)
    
    for role in all_roles:
        print(f"\n📌 {role}:")
        if role in role_permissions:
            modules = sorted(role_permissions[role])
            for module in modules:
                print(f"   ✓ {module}")
        else:
            print(f"   ✗ Sin acceso a ningún módulo")
        
        # Contar permisos
        count = len(role_permissions.get(role, []))
        total = len(PERMISSIONS)
        print(f"   Total: {count}/{total} módulos")
    
    print("\n" + "=" * 90)
    print("LEYENDA:")
    print("=" * 90)
    print("   ✓ = Tiene acceso (lectura y escritura)")
    print("   ✗ = Sin acceso")
    print("\n   ADMIN = ADMINISTRADOR")
    print("   SOPOR = SOPORTE")
    print("   VENDE = VENDEDOR")
    print("   CAJER = CAJERO")
    print("   ALMAC = ALMACEN")
    print("=" * 90)

if __name__ == '__main__':
    show_matrix()