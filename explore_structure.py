"""
Script para explorar la estructura del proyecto
Ejecutar con: python explore_structure.py
"""
import os
import glob

def explore_structure():
    print("=" * 70)
    print("ESTRUCTURA DEL PROYECTO PANDORA")
    print("=" * 70)
    
    # Buscar archivos Python en el directorio raíz
    print("\n📁 Archivos Python en la raíz:")
    root_files = glob.glob('*.py')
    for f in sorted(root_files):
        print(f"   {f}")
    
    # Buscar carpetas
    print("\n📁 Carpetas del proyecto:")
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and not item.startswith('.'):
            print(f"   {item}/")
    
    # Buscar archivos relacionados con modelos
    print("\n🔍 Buscando archivos de modelos:")
    model_files = glob.glob('**/models*.py', recursive=True) + glob.glob('**/model*.py', recursive=True)
    if model_files:
        for f in sorted(model_files):
            print(f"   ✓ {f}")
    else:
        print("   No se encontraron archivos de modelos")
    
    # Verificar si existe models.py o models/
    print("\n🔍 Verificando imports de modelos:")
    if os.path.exists('models.py'):
        print("   ✓ Encontrado: models.py (archivo único)")
    elif os.path.exists('models/__init__.py'):
        print("   ✓ Encontrado: models/ (paquete)")
        models_dir_files = glob.glob('models/*.py')
        for f in sorted(models_dir_files):
            print(f"      - {f}")
    else:
        print("   ⚠ No se encontró models.py ni models/")
    
    # Buscar archivos relacionados con Empleado
    print("\n🔍 Buscando referencias a Empleado:")
    all_py_files = glob.glob('**/*.py', recursive=True)
    empleado_files = []
    for f in all_py_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'class Empleado' in content:
                    empleado_files.append(f)
        except:
            pass
    
    if empleado_files:
        print("   Archivos que definen la clase Empleado:")
        for f in sorted(empleado_files):
            print(f"   ✓ {f}")
    else:
        print("   ⚠ No se encontró la definición de la clase Empleado")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    explore_structure()