# app/__init__.py

from flask import Flask
from flask_assets import Environment, Bundle

def create_app():
    app = Flask(__name__)

    # Load config
    if config_class:
        app.config.from_object(config_class)

    # Initialize Flask-Assets
    assets = Environment(app)
    assets.debug = False
    
    # Define asset bundles
    css = Bundle(
        'css/style.css',
        filters='cssmin',
        output='gen/style.min.css',
        depends='css/*.css'
    )
    # You can add multiple CSS files
    # css = Bundle(
    #     'css/style.css',
    #     'css/navbar.css',
    #     'css/responsive.css',
    #     filters='cssmin',
    #     output='gen/style.min.css'
    # )
    # Register bundles
    assets.register('css_all', css)
    # Optional: Configure cache settings
    app.config['ASSETS_CACHE'] = True
    app.config['ASSETS_AUTO_BUILD'] = True

    # Register blueprints here if needed
    # Example: from .views.main import main
    # Register blueprints
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    
    return app






