# app/__init__.py

from flask import Flask
from .cli import init_cli
from .assets import init_assets

def create_app(config_class=None):
    app = Flask(__name__)

    # Load config
    if config_class:
        app.config.from_object(config_class)

    # Initialize flask-assets
    init_assets(app)

    # Import and register CLI commands
    init_cli(app)

    # Register blueprints here if needed
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    
    return app






