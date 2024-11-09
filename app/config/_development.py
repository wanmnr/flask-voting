# app/config/_development.py
from app.config._default import DefaultConfig

class DevelopmentConfig(DefaultConfig):
    """Development configuration."""
    DEBUG = True
    DEVELOPMENT = True
    
    # Development-specific settings
    SQLALCHEMY_ECHO = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True