# app/config/_production.py
import os
from datetime import timedelta
from dotenv import load_dotenv
from app.config._default import DefaultConfig

load_dotenv()

class ProductionConfig(DefaultConfig):
    """Production configuration."""
    DEBUG = False
    TESTING = False

    # Production database settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://...'
    SQLALCHEMY_ECHO = False

    # Production cache settings
    REDIS_URL = 'redis://production-redis:6379'
    CACHE_TYPE = 'redis'

    # Production session settings
    SESSION_TYPE = "redis"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Production cookies settings
    REMEMBER_COOKIE_DURATION = timedelta(days=14)  # For "remember me" functionality

    # Production security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Production security headers settings
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }

    # Production File Upload settings (from .env)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

    # Production Celery settings (from .env)
    CELERY_BROKER_URL = os.getenv("REDIS_URL")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    # Production Mail settings (from .env)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") == "1"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Production Logging settings (from .env)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(os.getcwd(), 'instance', 'logs', 'app.log'))

    # Production API settings (from .env)
    API_TITLE = os.getenv("API_TITLE", "Voting System API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Production i18n / Internationalization & Localization settings (from .env)
    LANGUAGES = ["en", "es", "fr"]
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "UTC")

    # Production Rate Limiting settings (from .env)
    RATELIMIT_DEFAULT = "200 per day;50 per hour;1 per second"
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL")
    RATELIMIT_STRATEGY = "fixed-window"

    # Production WebSocket settings (from .env)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("REDIS_URL")

    # Production Feature Flags settings (from .env)
    FEATURE_FLAGS = {
        'ENABLE_REGISTRATION': os.getenv("ENABLE_REGISTRATION", "1") == "1",
        'ENABLE_OAUTH': os.getenv("ENABLE_OAUTH", "0") == "1",
        'ENABLE_2FA': os.getenv("ENABLE_2FA", "0") == "1",
        'ENABLE_FILE_UPLOAD': os.getenv("ENABLE_FILE_UPLOAD", "1") == "1",
    }

    # Production Admin Interface settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Production Debug Toolbar settings (from .flaskenv)
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Production Assets settings (from .flaskenv)
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True

    # Production Feature Flags settings
    FEATURE_NEW_UI = False
    FEATURE_BETA = False
    FEATURE_PREMIUM = True
