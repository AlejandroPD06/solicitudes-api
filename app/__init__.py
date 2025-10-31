"""Factory pattern para la aplicación Flask."""
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_admin import Admin
from flasgger import Swagger
from config import config_by_name
from werkzeug.exceptions import HTTPException

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()
# Admin se inicializa en create_app con el index_view personalizado
admin_instance = None


def create_app(config_name=None):
    """
    Factory pattern para crear la aplicación Flask.

    Args:
        config_name: Nombre de la configuración a usar (development, production, testing)

    Returns:
        Flask app configurada
    """
    # Crear instancia de Flask
    app = Flask(__name__)

    # Cargar configuración
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Inicializar Flask-Admin con index view personalizado
    from app.admin.views import CustomAdminIndexView
    global admin_instance
    admin_instance = Admin(
        app,
        name='Solicitudes Admin',
        template_mode='bootstrap4',
        index_view=CustomAdminIndexView(name='Dashboard', url='/admin')
    )

    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configurar Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Solicitudes",
            "description": "Documentación interactiva de la API del Sistema de Solicitudes. Permite gestionar usuarios, solicitudes y notificaciones.",
            "version": "1.0.0",
            "contact": {
                "name": "Equipo de Desarrollo",
                "email": "admin@solicitudes.com"
            }
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header usando el esquema Bearer. Ejemplo: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}],
        "tags": [
            {"name": "Autenticación", "description": "Endpoints de login y gestión de usuarios"},
            {"name": "Solicitudes", "description": "CRUD de solicitudes"},
            {"name": "Notificaciones", "description": "Sistema de notificaciones"},
            {"name": "Sistema", "description": "Health check y utilidades"}
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.solicitudes import solicitudes_bp
    from app.routes.notificaciones import notificaciones_bp
    from app.routes.frontend import frontend_bp

    app.register_blueprint(auth_bp, url_prefix='/api/usuarios')
    app.register_blueprint(solicitudes_bp, url_prefix='/api/solicitudes')
    app.register_blueprint(notificaciones_bp, url_prefix='/api/notificaciones')
    app.register_blueprint(frontend_bp, url_prefix='/app')

    # Configurar Flask-Admin
    from app.admin.views import configure_admin
    configure_admin(admin_instance, db)

    # Configurar logging
    from app.utils.logger import setup_logger
    setup_logger(app)

    # Registrar error handlers
    register_error_handlers(app)

    # Ruta de health check
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'solicitudes-api'}, 200

    @app.route('/')
    def index():
        """Ruta principal - redirige al portal de empleados."""
        from flask import redirect, url_for
        return redirect(url_for('frontend.index'))

    return app


def register_error_handlers(app):
    """
    Registra manejadores globales de errores para la aplicación.

    Args:
        app: Instancia de Flask
    """
    from app.exceptions import APIException
    from app.utils.responses import error_response
    from app.utils.logger import log_error
    from flask_jwt_extended.exceptions import JWTExtendedException

    @app.errorhandler(APIException)
    def handle_api_exception(error):
        """Maneja todas las excepciones personalizadas de la API."""
        log_error(
            f"APIException: {error.error_code}",
            error_code=error.error_code,
            message=error.message,
            details=error.details,
            status_code=error.status_code
        )

        return error_response(
            error_code=error.error_code,
            message=error.message,
            status_code=error.status_code,
            details=error.details if error.details else None
        )

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exception(error):
        """Maneja errores de JWT."""
        log_error(f"JWT Error: {str(error)}", exception=error)

        return error_response(
            error_code='JWT_ERROR',
            message=str(error),
            status_code=401
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Maneja excepciones HTTP estándar de Werkzeug."""
        log_error(
            f"HTTP Error {error.code}: {error.name}",
            status_code=error.code,
            description=error.description
        )

        return error_response(
            error_code=error.name.upper().replace(' ', '_'),
            message=error.description or error.name,
            status_code=error.code
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        """Maneja errores 404 Not Found."""
        return error_response(
            error_code='NOT_FOUND',
            message='El recurso solicitado no fue encontrado',
            status_code=404
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Maneja errores 405 Method Not Allowed."""
        return error_response(
            error_code='METHOD_NOT_ALLOWED',
            message='El método HTTP no está permitido para este endpoint',
            status_code=405
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Maneja errores 500 Internal Server Error."""
        log_error(
            "Internal Server Error",
            exception=error,
            critical=True
        )

        # En producción, no exponer detalles del error
        if app.config.get('DEBUG'):
            message = str(error)
        else:
            message = 'Ha ocurrido un error interno en el servidor'

        return error_response(
            error_code='INTERNAL_SERVER_ERROR',
            message=message,
            status_code=500
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Maneja cualquier excepción no capturada."""
        log_error(
            "Unexpected Error",
            exception=error,
            error_type=type(error).__name__,
            critical=True
        )

        # Rollback de base de datos en caso de error
        try:
            db.session.rollback()
        except:
            pass

        # En producción, no exponer detalles del error
        if app.config.get('DEBUG'):
            message = f'{type(error).__name__}: {str(error)}'
        else:
            message = 'Ha ocurrido un error inesperado'

        return error_response(
            error_code='UNEXPECTED_ERROR',
            message=message,
            status_code=500
        )
