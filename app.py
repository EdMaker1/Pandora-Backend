from flask import Flask, send_from_directory, jsonify, make_response
from config import Config
from models import db
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from datetime import timedelta
import os

from routes.auth_google import auth_google_bp, init_google
from routes.auth import auth_bp
from routes.categorias import categorias_bp
from routes.productos import productos_bp
from routes.empleados import empleados_bp
from routes.clientes import clientes_bp
from routes.ventas import ventas_bp
from routes.reportes import reportes_bp
from routes.stock_adjustment import stock_bp
from routes.pagos import pagos_bp

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    
    # ============================================================
    # CONFIGURACIÓN DE COOKIES PARA DESARROLLO Y PRODUCCIÓN
    # ============================================================
    app.config['SESSION_COOKIE_NAME'] = 'pandora_session'
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Importante: string 'None', no Python None
    app.config['SESSION_COOKIE_HTTPONLY'] = True    # Más seguro
    app.config['SESSION_COOKIE_SECURE'] = True      # Requerido para SameSite=None con HTTPS
    app.config['SESSION_COOKIE_PATH'] = '/'
    app.config['SESSION_COOKIE_DOMAIN'] = None      # No restringir dominio
    # ============================================================

    # ============================================================
    # CORS DINÁMICO - DESARROLLO Y PRODUCCIÓN
    # ============================================================
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Lista de orígenes permitidos
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Agregar URL de producción si existe y es diferente
    if FRONTEND_URL and FRONTEND_URL not in allowed_origins:
        allowed_origins.append(FRONTEND_URL)
    
    print(f"🌐 CORS configurado para orígenes: {allowed_origins}")
    
    CORS(app, 
         resources={r"/*": {"origins": allowed_origins}},
         supports_credentials=True,
         allow_headers=["Content-Type"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    # ============================================================

    db.init_app(app)
    migrate = Migrate(app, db)

    init_google(app)
    app.register_blueprint(auth_google_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(empleados_bp, url_prefix='/api/empleados')
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(ventas_bp, url_prefix='/api/ventas')
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
    app.register_blueprint(stock_bp, url_prefix='/api/stock_adjustments')
    app.register_blueprint(pagos_bp, url_prefix='/api/pagos')

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API Librería Pandora"})
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    @app.route('/openapi.json')
    def openapi():
        response = make_response(send_from_directory('static', 'swagger.json'))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route("/docs")
    def swagger_ui_html():
        return send_from_directory('static', 'swagger_ui.html')

    @app.route('/')
    def index():
        return '''<h2>✨ API Pandora</h2>
                  <p>Backend en la nube</p>
                  <ul>
                      <li><a href="/docs">/docs</a> - Documentación</li>
                      <li>POST /api/auth/login - Login</li>
                      <li>GET /api/auth/me - Usuario actual</li>
                      <li>GET /auth/google/login - Login con Google</li>
                  </ul>'''

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Error interno"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)