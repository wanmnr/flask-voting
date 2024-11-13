# app/__init__.py
import os
from flask import Flask, request, session
from .config import configs
from .extensions import db, migrate, login_manager, init_login_manager, assets
from .models.user import User  # Your models
from .core.errors import register_error_handlers
from .utils.utils import get_context_processors
from .cli import register_commands

def create_app(config_name=None):
    """Create application factory."""
    app = Flask(__name__)

    # Load default configuration
    app.config.from_object(configs['default'])

    # Override with environment-specific configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    if config_name in configs:
        app.config.from_object(configs[config_name])

    # Optional: Override with instance configuration file if it exists
    instance_config = os.path.join(app.instance_path, 'config.py')
    if os.path.exists(instance_config):
        app.config.from_pyfile(instance_config)

    # Initialize login manager first
    with app.app_context():
        assets.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        init_login_manager(app)

    # Cross-extension setup
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register error handlers
    register_error_handlers(app)

    # Register cli commands
    register_commands(app)

    # Register context processor
    app.context_processor(get_context_processors())

    # Initialize Babel with locale selector
    # babel.init_app(app, locale_selector=get_locale)

    # Register blueprints
    from app.views import register_blueprints
    register_blueprints(app)

    return app
