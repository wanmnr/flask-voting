class Config:
    # Base config
    ASSETS_DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True  # Disable minification during development

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False  # Enable minification in production