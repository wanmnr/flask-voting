# app/views/__init__.py
from flask import Blueprint
from app.views.main import main_bp
from app.views.auth import auth_bp
from app.views.admin import admin_bp
from app.views.api import api_bp
from app.views.polls import polls_bp

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(polls_bp, url_prefix='/polls')