# app/core/features.py

from functools import wraps
from flask import current_app, abort

def feature_required(feature_name):
    """Decorator to check if a feature is enabled."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.config['FEATURE_FLAGS'].get(feature_name):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example:
# @feature_required('ENABLE_2FA')
# def two_factor_auth():
#     pass