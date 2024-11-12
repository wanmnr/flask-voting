# app/__init__.py

from flask import Flask, request, session
from .extensions import init_db, login_manager, init_login_manager, init_assets
from .models.user import User  # Your models
from .core.errors import register_error_handlers
from .utils.utils import get_context_processors

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

    # Initialize login manager first
    with app.app_context():
        init_assets(app)
        init_db(app)
        init_login_manager(app)

    # Cross-extension setup
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize extensions
    # extensions = [
    #     db, assets, mail,
    #     limiter, jwt, csrf
    # ]
    # for extension in extensions:
    #     extension.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register cli commands
    # register_commands(app)

    # Register context processor
    app.context_processor(get_context_processors())

    # Initialize Babel with locale selector
    # babel.init_app(app, locale_selector=get_locale)

    # Register blueprints
    from app.views import register_blueprints
    register_blueprints(app)

    return app
