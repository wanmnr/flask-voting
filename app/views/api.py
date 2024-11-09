# app/views/api.py
from flask import Blueprint, jsonify
from app.core.extensions import limiter, jwt
from flask_jwt_extended import jwt_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
@limiter.limit("60 per minute")
def status():
    return jsonify({'status': 'operational'})

@api_bp.route('/protected-data')
@jwt_required()
@limiter.limit("30 per minute")
def protected_data():
    return jsonify({'data': 'sensitive information'})