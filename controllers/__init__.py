import os
import sys

from flask import Flask
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

    return app
