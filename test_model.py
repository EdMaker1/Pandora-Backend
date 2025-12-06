"""
Script para verificar el modelo Empleado y sus métodos
Ejecutar con: python check_model.py
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

try:
    from models.empleado import Empleado
    
    print("=" * 70)
    print("VERIFICACIÓN DEL MODELO EMPLEADO")
    print("=" * 70)
    
    print("\n✓ Modelo Empleado importado correctamente")
    
    # Verificar si existe el método check_password
    if hasattr(Empleado, 'check_password'):
        print("✓ El método 'check_password' existe")
        
        # Mostrar el código del método
        import inspect
        print("\nCódigo del método check_password:")
        print("-" * 70)
        try:
            source = inspect.getsource(Empleado.check_password)
            print(source)
        except:
            print("(No se pudo obtener el código fuente)")
    else:
        print("❌ El método 'check_password' NO existe")
        print("\nMétodos disponibles en el modelo Empleado:")
        methods = [method for method in dir(Empleado) if not method.startswith('_')]
        for method in methods:
            print(f"   - {method}")
    
    # Verificar si existe set_password
    if hasattr(Empleado, 'set_password'):
        print("\n✓ El método 'set_password' existe")
    else:
        print("\n⚠ El método 'set_password' NO existe")
    
    print("\n" + "=" * 70)
    
except ImportError as e:
    print(f"❌ Error al importar el modelo: {e}")
    print("\nIntentando encontrar el archivo del modelo...")
    
    import glob
    models_files = glob.glob('models/*.py')
    print("\nArchivos en la carpeta models:")
    for f in models_files:
        print(f"   - {f}")