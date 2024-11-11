# core/feature_flags.py
from enum import Enum
from typing import Dict, Optional
from functools import wraps
from flask import current_app, abort

class Feature(Enum):
    NEW_UI = "new_ui"
    BETA_FEATURE = "beta_feature"
    PREMIUM_USERS = "premium_users"

class FeatureFlags:
    def __init__(self):
        self._flags: Dict[str, bool] = {}

    def init_app(self, app):
        self._flags = {
            Feature.NEW_UI.value: app.config.get('FEATURE_NEW_UI', False),
            Feature.BETA_FEATURE.value: app.config.get('FEATURE_BETA', False),
            Feature.PREMIUM_USERS.value: app.config.get('FEATURE_PREMIUM', False),
        }
        app.feature_flags = self

    def is_enabled(self, feature: Feature) -> bool:
        return self._flags.get(feature.value, False)

    def enable(self, feature: Feature):
        self._flags[feature.value] = True

    def disable(self, feature: Feature):
        self._flags[feature.value] = False

# Decorator for feature flag checking
def feature_required(feature: Feature):
    """Decorator to check if a feature is enabled."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.feature_flags.is_enabled(feature):
                abort(404)  # Or handle differently
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example:
# @feature_required('ENABLE_2FA')
# def two_factor_auth():
#     pass




# core/feature_flags.py
# from .extensions import db

# class FeatureFlag(db.Model):
#     __tablename__ = 'feature_flags'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     enabled = db.Column(db.Boolean, default=False)
#     description = db.Column(db.String(200))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class DatabaseFeatureFlags:
#     def init_app(self, app):
#         app.feature_flags = self

#     def is_enabled(self, feature: Feature) -> bool:
#         flag = FeatureFlag.query.filter_by(name=feature.value).first()
#         return flag.enabled if flag else False

#     def enable(self, feature: Feature):
#         flag = FeatureFlag.query.filter_by(name=feature.value).first()
#         if flag:
#             flag.enabled = True
#             db.session.commit()

#     def disable(self, feature: Feature):
#         flag = FeatureFlag.query.filter_by(name=feature.value).first()
#         if flag:
#             flag.enabled = False
#             db.session.commit()
