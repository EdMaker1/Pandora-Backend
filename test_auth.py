"""
Script para probar la autenticación de usuarios
Ejecutar con: python test_auth.py
"""
import sqlite3
from werkzeug.security import check_password_hash

def test_authentication():
    """Prueba la autenticación de usuarios"""
    
    db_path = 'instance/Pandora.db'
    
    print("=" * 70)
    print("PRUEBA DE AUTENTICACIÓN")
    print("=" * 70)
    
    # Credenciales a probar
    test_credentials = [
        ('sa', '12345678'),
        ('lgarcía2f', 'password123'),
        ('lgarcía3f', 'password123'),
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for username, password in test_credentials:
        print(f"\n🔍 Probando usuario: {username}")
        print(f"   Contraseña: {password}")
        
        # Buscar usuario
        cursor.execute("""
            SELECT id, username, password_hash, activo, rol 
            FROM empleado 
            WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        
        if not user:
            print(f"   ❌ Usuario '{username}' no encontrado")
            continue
        
        user_id, db_username, password_hash, activo, rol = user
        
        print(f"   ✓ Usuario encontrado (ID: {user_id})")
        print(f"   - Rol: {rol}")
        print(f"   - Activo: {'Sí' if activo else 'No'}")
        print(f"   - Password hash: {password_hash[:50]}...")
        
        # Verificar si está activo
        if not activo:
            print(f"   ❌ El usuario está INACTIVO")
            continue
        
        # Verificar contraseña
        if password_hash:
            try:
                if check_password_hash(password_hash, password):
                    print(f"   ✅ Contraseña CORRECTA")
                else:
                    print(f"   ❌ Contraseña INCORRECTA")
            except Exception as e:
                print(f"   ❌ Error al verificar contraseña: {e}")
        else:
            print(f"   ❌ Usuario sin contraseña configurada")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("RECOMENDACIONES:")
    print("=" * 70)
    print("""
    Si las contraseñas son correctas pero no puedes iniciar sesión:
    
    1. Verifica el endpoint de login en routes/auth.py
    2. Revisa la consola del navegador (F12) para ver errores
    3. Verifica que el frontend esté enviando correctamente los datos
    4. Asegúrate de que CORS esté configurado correctamente
    """)

if __name__ == '__main__':
    test_authentication()