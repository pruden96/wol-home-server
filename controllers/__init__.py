from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.device_controller import device_bp
from controllers.wol_controller import wol_bp
from controllers.user_controller import user_bp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder='../templates')
    app.secret_key = Config.SECRET_KEY  # Cargar la clave secreta desde config.py

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(wol_bp)
    app.register_blueprint(user_bp)

    return app