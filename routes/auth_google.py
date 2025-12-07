from flask import Blueprint, redirect, url_for, session, jsonify, request
from authlib.integrations.flask_client import OAuth
from models import db, Empleado
import traceback
import os
import secrets

auth_google_bp = Blueprint("auth_google", __name__, url_prefix="/auth/google")
oauth = OAuth()

# URL del frontend (producción o desarrollo)
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Almacenar tokens temporales (en producción usar Redis)
temp_tokens = {}

def init_google(app):
    """Inicializa Google OAuth"""
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"}
    )
    print(f"🔐 Google OAuth inicializado - Frontend URL: {FRONTEND_URL}")

@auth_google_bp.route("/login")
def login():
    """Inicia el flujo de autenticación de Google"""
    print("🔵 Iniciando flujo de Google OAuth")
    redirect_uri = url_for("auth_google.authorize", _external=True)
    print(f"🔵 Redirect URI: {redirect_uri}")
    return oauth.google.authorize_redirect(redirect_uri)

@auth_google_bp.route("/authorize")
def authorize():
    """Callback de Google OAuth - procesa la autenticación"""
    print("=" * 70)
    print("🔍 ENTRANDO A /auth/google/authorize")
    print("=" * 70)
    
    try:
        # Obtener token y datos del usuario
        print("📡 Obteniendo token de Google...")
        token = oauth.google.authorize_access_token()
        print(f"✅ Token obtenido")
        
        user_info = token.get('userinfo')
        if not user_info:
            print("❌ ERROR: No se pudo obtener userinfo del token")
            return redirect(f"{FRONTEND_URL}/login?error=no_userinfo")
        
        google_id = user_info.get("sub")
        google_email = user_info.get("email")
        google_name = user_info.get("name")
        google_picture = user_info.get("picture")
        
        print(f"✅ Información del usuario obtenida:")
        print(f"   - Google ID: {google_id}")
        print(f"   - Email: {google_email}")
        print(f"   - Nombre: {google_name}")
        
        # Buscar empleado
        print(f"🔍 Buscando empleado con email: {google_email}")
        empleado = Empleado.query.filter(
            (Empleado.google_id == google_id) | 
            (Empleado.email == google_email)
        ).first()
        
        if not empleado:
            print(f"❌ No se encontró empleado con email {google_email}")
            return redirect(f"{FRONTEND_URL}/login?error=no_account&email={google_email}")
        
        print(f"✅ Empleado encontrado: {empleado.username} (ID: {empleado.id})")
        
        # Vincular cuenta de Google si no estaba vinculada
        if not empleado.google_id:
            print("🔗 Vinculando cuenta de Google...")
            empleado.google_id = google_id
            empleado.google_email = google_email
            empleado.google_picture = google_picture
            db.session.commit()
            print("✅ Cuenta vinculada")
        
        # Verificar que esté activo
        if not empleado.activo:
            print(f"❌ El empleado está inactivo")
            return redirect(f"{FRONTEND_URL}/login?error=account_disabled")
        
        # Crear sesión en el backend
        print("�� Creando sesión...")
        session.permanent = True
        session['user_id'] = empleado.id
        session['username'] = empleado.username
        session['rol'] = empleado.rol
        session['nombre_completo'] = f"{empleado.primer_nombre} {empleado.apellido_paterno}"
        session['google_picture'] = google_picture
        session['login_method'] = 'google'
        
        # Generar token temporal para el frontend
        temp_token = secrets.token_urlsafe(32)
        temp_tokens[temp_token] = {
            'user_id': empleado.id,
            'username': empleado.username,
            'rol': empleado.rol,
            'nombre_completo': session['nombre_completo'],
            'picture': google_picture,
            'login_method': 'google'
        }
        
        print(f"✅ Sesión creada y token generado: {temp_token[:16]}...")
        print(f"🔄 Redirigiendo a {FRONTEND_URL}/?token={temp_token[:16]}...")
        
        # Redirigir al frontend con el token
        return redirect(f"{FRONTEND_URL}/?token={temp_token}")
        
    except Exception as e:
        print("=" * 70)
        print(f"❌ ERROR EN GOOGLE OAUTH: {str(e)}")
        traceback.print_exc()
        print("=" * 70)
        return redirect(f"{FRONTEND_URL}/login?error=auth_failed")

@auth_google_bp.route("/exchange-token", methods=['POST'])
def exchange_token():
    """Intercambia un token temporal por datos de sesión"""
    data = request.get_json()
    token = data.get('token')
    
    print(f"🔄 Recibida petición de intercambio de token: {token[:16] if token else 'None'}...")
    
    if not token or token not in temp_tokens:
        print("❌ Token inválido o expirado")
        return jsonify({"error": "Token inválido o expirado"}), 401
    
    # Obtener datos del token
    user_data = temp_tokens.pop(token)  # Eliminar token después de usarlo
    print(f"✅ Token intercambiado exitosamente para usuario: {user_data.get('username')}")
    
    return jsonify(user_data), 200

@auth_google_bp.route("/logout")
def logout():
    """Cierra sesión"""
    session.clear()
    return redirect(f"{FRONTEND_URL}/login")
