# app/config/_development.py
from app.config._default import DefaultConfig

class DevelopmentConfig(DefaultConfig):
    """Development configuration."""
    DEBUG = True
    DEVELOPMENT = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    REDIS_URL = 'redis://localhost:6379'
    CACHE_TYPE = 'redis'

    # Development-specific settings
    SQLALCHEMY_ECHO = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True

    # Featire Flags settings
    FEATURE_NEW_UI = True
    FEATURE_BETA = True
    FEATURE_PREMIUM = False
