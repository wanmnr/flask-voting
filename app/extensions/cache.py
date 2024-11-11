# app/extensions/cache_config.py

from flask_caching import Cache

cache = Cache()

def init_cache(app):
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': app.config['REDIS_URL']
    }
    cache.init_app(app, config=cache_config)


# setup/cache.py
from ..app_extensions import cache
from typing import Optional
from flask import Flask

def init_cache(app: Flask, redis_url: Optional[str] = None) -> None:
    """Initialize caching with Redis configuration"""
    config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': redis_url or app.config['REDIS_URL'],
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_KEY_PREFIX': 'myapp:',
    }
    cache.init_app(app, config=config)



def init_cache(app):
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': app.config['REDIS_URL']
    }
    cache.init_app(app, config=cache_config)
