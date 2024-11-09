# config.py

import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Base config
    ASSETS_DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    REDIS_URI = os.environ.get('REDIS_URL')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'voting_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REMEMBER_COOKIE_DURATION = timedelta(days=14)  # For "remember me" functionality

    # Babel configuration
    LANGUAGES = ['en', 'es', 'fr']
    BABEL_DEFAULT_LOCALE = os.environ.get('BABEL_DEFAULT_LOCALE') or 'en'
    BABEL_DEFAULT_TIMEZONE = os.environ.get('BABEL_DEFAULT_TIMEZONE') or 'UTC'

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True  # Disable minification during development

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False  # Enable minification in production