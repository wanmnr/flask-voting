# app/extensions/cache.py

from flask_caching import Cache
from typing import Optional, Type
from flask import Flask
import importlib
from app.config._default import DefaultConfig

cache = Cache()

def get_config_class(config_name: str) -> Type[DefaultConfig]:
    """Dynamically import and return the config class based on environment"""
    try:
        module = importlib.import_module(f'app.config._{config_name.lower()}')
        return getattr(module, f'{config_name.capitalize()}Config')
    except (ImportError, AttributeError):
        # Fallback to default config if specified config doesn't exist
        from app.config._default import DefaultConfig
        return DefaultConfig

def init_cache(app: Flask, redis_url: Optional[str] = None) -> None:
    """Initialize caching with Redis configuration"""
    # Get the config class based on the app's config
    env = app.config.get('ENV', 'default')
    config_class = get_config_class(env)
    config = config_class()

    cache_config = {
        'CACHE_TYPE': config.CACHE_TYPE,
        'CACHE_REDIS_URL': redis_url or config.CACHE_REDIS_URL,
        'CACHE_DEFAULT_TIMEOUT': config.CACHE_DEFAULT_TIMEOUT,
        'CACHE_KEY_PREFIX': 'voting:',
    }
    cache.init_app(app, config=cache_config)
