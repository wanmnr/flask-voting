# app/__init__.py

from flask import Flask
from flask_assets import Environment, Bundle
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)

    # Initialize Flask-Assets
    assets = Environment(app)
    
    # Define asset bundles
    css = Bundle(
        'css/style.css',
        filters='cssmin',
        output='gen/packed.css'
    )
    # Register bundles
    assets.register('css_all', css)

    # Register blueprints here if needed
    # Example: from .views.main import main
    # Register blueprints
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    
    return app






