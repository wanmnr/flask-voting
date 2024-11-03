# app/__init__.py

from flask import Flask
from .extensions import db, login_manager
from .cli import init_cli
from .assets import init_assets

@login_manager.user_loader
def load_user(id):
    from .models import User  # Import here to avoid circular import
    return User.query.get(int(id))

def create_app(config_class=None):
    app = Flask(__name__)

    # Load config
    if config_class:
        app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Initialize flask-assets
    init_assets(app)

    # Import and register CLI commands
    init_cli(app)

    # Register blueprints
    from app.views.main import main_bp
    from app.views.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    
    return app






