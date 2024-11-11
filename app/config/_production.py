# app/config/_production.py
from app.config._default import DefaultConfig

class ProductionConfig(DefaultConfig):
    """Production configuration."""
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://...'
    REDIS_URL = 'redis://production-redis:6379'
    CACHE_TYPE = 'redis'

    # Production-specific settings
    SQLALCHEMY_ECHO = False
    DEBUG_TB_ENABLED = False
    ASSETS_DEBUG = False

    # Enhanced security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Featire Flags settings
    FEATURE_NEW_UI = False
    FEATURE_BETA = False
    FEATURE_PREMIUM = True
