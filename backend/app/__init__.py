# backend/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow  # Asegúrate de importar Marshmallow
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()  # Asegúrate de inicializar Marshmallow

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_object(Config)

    # Inicialización de extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)  # Inicialización de Marshmallow

    from .routes import main
    app.register_blueprint(main)

    return app
