import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_login import LoginManager

from app.extensions import db
from app.models.models import User

from config import Config

def create_app():
    app = Flask(__name__)
    
    env_config = os.getenv("PROD_APP_SETTINGS", "config.Config")
    app.config.from_object(env_config)
    
    # Initialize Flask extensions here
    db.init_app(app)
    login_manager.init_app(app)

    # Configure the logging
    app.logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Register the blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.user import bp as user_bp
    app.register_blueprint(user_bp)
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

   
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

login_manager = LoginManager()
login_manager.login_view = 'user.login'
