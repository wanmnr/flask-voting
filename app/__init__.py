# app/__init__.py

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    # Register blueprints here if needed
    # Example: from .views.main import main
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app






