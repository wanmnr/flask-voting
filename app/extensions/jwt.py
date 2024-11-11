# app/extensions/jwt.py
from ..app_extensions import jwt
from flask import Flask, jsonify
from ..models.user import User

def init_jwt(app: Flask) -> None:
    """Initialize JWT with error handlers and callbacks"""

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 401,
            'message': 'Token has expired'
        }), 401

    jwt.init_app(app)
