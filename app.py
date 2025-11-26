from flask import Flask, send_from_directory, jsonify, make_response
from config import Config
from models import db
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Importar Google SSO
from routes.auth_google import auth_google_bp, init_google

# Importar Blueprints API
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

    # Habilitar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Inicializar SSO Google
    init_google(app)
    app.register_blueprint(auth_google_bp)

    # Registrar Blueprints API (sin /api en las rutas porque ya está en url_prefix)
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(empleados_bp, url_prefix='/api/empleados')
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(ventas_bp, url_prefix='/api/ventas')
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
    app.register_blueprint(stock_bp, url_prefix='/api/stock_adjustments')
    app.register_blueprint(pagos_bp, url_prefix='/api/pagos')

    # Swagger UI estándar (/swagger)
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "API Librería Pandora"}
    )
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    # Servir OpenAPI JSON
    @app.route('/openapi.json')
    def openapi():
        response = make_response(send_from_directory('static', 'swagger.json'))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Servir Swagger UI personalizado (/docs)
    @app.route("/docs")
    def swagger_ui_html():
        return send_from_directory('static', 'swagger_ui.html')

    # Página raíz
    @app.route('/')
    def index():
        return '''<h2>✨ Bienvenido a la API Pandora</h2>
                  <p>Documentación disponible en:</p>
                  <ul>
                      <li><a href="/swagger">/swagger</a> - Swagger UI estándar</li>
                      <li><a href="/docs">/docs</a> - Swagger UI personalizado</li>
                      <li><a href="/auth/login">/auth/login</a> - Login con Google</li>
                      <li><a href="/auth/me">/auth/me</a> - Ver usuario logueado</li>
                  </ul>
                  <h3>Endpoints API:</h3>
                  <ul>
                      <li>/api/categorias</li>
                      <li>/api/productos</li>
                      <li>/api/empleados</li>
                      <li>/api/clientes</li>
                      <li>/api/ventas</li>
                      <li>/api/pagos</li>
                      <li>/api/stock_adjustments</li>
                      <li>/api/reportes</li>
                  </ul>'''

    # Manejo de errores
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app

# Instancia global para Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)