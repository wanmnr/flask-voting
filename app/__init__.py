# app/__init__.py

from flask import Flask, request, session
from app.cli import register_commands
# from flask_babel import Babel
from app.core.extensions import (
    db, init_assets, login_manager, migrate, assets, cache, mail, 
    limiter, jwt, csrf
)

from app.core.errors import register_error_handlers
# from app.core.security import configure_security
from app.core.auth import init_login_manager
from app.cli import register_commands
from app.utils.utils import get_context_processors

# Initialize Babel for internationalization
# babel = Babel()

# def get_locale():
#     if 'language' in session:
#         return session['language']
#     return request.accept_languages.best_match(['en', 'es', 'fr'])

def create_app(config_object):
    """Create application factory."""
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration
    app.config.from_object(config_object)
    
    # Load instance config if it exists
    app.config.from_pyfile('config.py', silent=True)

    # Register context processor
    app.context_processor(get_context_processors())

    # Initialize extensions
    extensions = [
        db, login_manager, cache, mail,
        limiter, jwt, csrf
    ]
    for extension in extensions:
        extension.init_app(app)
    
    # Special initializations
    migrate.init_app(app, db)
    init_assets(app)
    init_login_manager(app)

    # Configure security
    # configure_security(app)

    # Register error handlers
    register_error_handlers(app)

    # Initialize Babel with locale selector
    # babel.init_app(app, locale_selector=get_locale)

    # Register CLI commands
    register_commands(app)

    # Register blueprints
    from app.views import register_blueprints
    register_blueprints(app)
    
    return app
