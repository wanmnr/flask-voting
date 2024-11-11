# app/config/__init__.py
from app.config._default import DefaultConfig
from app.config._development import DevelopmentConfig
from app.config._production import ProductionConfig

# Map environment names to config classes using Dictionary approach
configs = {
    'default': DefaultConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
