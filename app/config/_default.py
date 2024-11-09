# app/config/_default.py
class DefaultConfig:
    """Base configuration."""
    # Default settings that are common across all environments
    APP_NAME = "Voting System"
    TESTING = False
    
    # Default database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Default cache settings
    CACHE_TYPE = "simple"
    
    # Default mail settings
    MAIL_USE_TLS = True
    
    # Default security settings
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour