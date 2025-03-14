import logging
import os
import sys

from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from controllers.auth_controller import auth_bp
from controllers.camera_controller import camera_bp
from controllers.device_controller import device_bp
from controllers.user_controller import user_bp
from controllers.wol_controller import wol_bp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config


def create_app() -> Flask:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.secret_key = Config.SECRET_KEY  # Cargar la clave secreta desde config.py
    CORS(app, supports_credentials=True)  # Permite cookies en solicitudes POST

    # Configuración de JWT con cookies HTTP-Only
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY  # Clave secreta
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Almacenar JWT en cookies
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"  # Nombre de la cookie
    app.config["JWT_COOKIE_SECURE"] = False  # En local, debe ser False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Para pruebas, desactivar CSRF

    jwt = JWTManager(app)  # Inicializar JWTManager  # noqa: F841

    # Manejar errores de autenticación
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        print("Unauthorized callback")
        return redirect(url_for("auth.login"))  # Redirige a login si no hay token

    # @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("Expired token callback")
        return redirect(url_for("auth.login"))  # Redirige a login si el token expiró

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(wol_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(camera_bp)

    # Configuración de Swagger UI
    SWAGGER_URL = "/apidocs"
    API_URL = "/static/swagger.yml"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "API de Gestión de Dispositivos Wake On LAN (WoL)"},
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)  # Establecer nivel de logging para la app

    return app
