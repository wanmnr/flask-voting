# app/views/__init__.py
from flask import Blueprint
from app.views.main import main_bp
from app.views.auth import auth_bp
from app.views.admin import myadmin_bp
from app.views.polls import polls_bp
from app.views.users import users_bp
from app.views.mock_error import mock_bp

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(myadmin_bp, url_prefix='/admin')
    app.register_blueprint(polls_bp, url_prefix='/polls')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(mock_bp, url_prefix='/mock')
