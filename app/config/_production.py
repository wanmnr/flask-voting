# app/config/_production.py
from app.config._default import DefaultConfig

class ProductionConfig(DefaultConfig):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SQLALCHEMY_ECHO = False
    DEBUG_TB_ENABLED = False
    ASSETS_DEBUG = False
    
    # Enhanced security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True