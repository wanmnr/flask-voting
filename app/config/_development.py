# app/config/_development.py
import os
from datetime import timedelta
from dotenv import load_dotenv
from app.config._default import DefaultConfig

load_dotenv()

class DevelopmentConfig(DefaultConfig):
    """Development configuration."""
    # Environment
    DEBUG = True
    TESTING = True

    # Development database settings
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
    SQLALCHEMY_ECHO = True

    # Development cache settings
    CACHE_TYPE = os.getenv("CACHE_TYPE", "redis")
    CACHE_REDIS_URL = os.getenv('REDIS_URL', "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 300

    # Development session settings
    SESSION_TYPE = "redis"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Development cookies settings
    REMEMBER_COOKIE_DURATION = timedelta(days=14)  # For "remember me" functionality

    # Development security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Development security headers settings
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }

    # Development File Upload settings (from .env)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

    # Development Celery settings (from .env)
    CELERY_BROKER_URL = os.getenv("REDIS_URL")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    # Development Mail settings (from .env)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") == "1"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Development Logging settings (from .env)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(os.getcwd(), 'instance', 'logs', 'app.log'))

    # Development API settings (from .env)
    API_TITLE = os.getenv("API_TITLE", "Voting System API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Development i18n / Internationalization & Localization settings (from .env)
    LANGUAGES = ["en", "es", "fr"]
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "UTC")

    # Development Rate Limiting settings (from .env)
    RATELIMIT_DEFAULT = "200 per day;50 per hour;1 per second"
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL")
    RATELIMIT_STRATEGY = "fixed-window"

    # Development WebSocket settings (from .env)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("REDIS_URL")

    # Development Feature Flags settings (from .env)
    FEATURE_FLAGS = {
        'ENABLE_REGISTRATION': os.getenv("ENABLE_REGISTRATION", "1") == "1",
        'ENABLE_OAUTH': os.getenv("ENABLE_OAUTH", "0") == "1",
        'ENABLE_2FA': os.getenv("ENABLE_2FA", "0") == "1",
        'ENABLE_FILE_UPLOAD': os.getenv("ENABLE_FILE_UPLOAD", "1") == "1",
    }

    # Development Admin Interface settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Development Debug Toolbar settings (from .flaskenv)
    DEBUG_TB_ENABLED = os.getenv("FLASK_ENV") == "development"
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Development Assets settings (from .flaskenv)
    ASSETS_DEBUG = os.getenv("ASSETS_DEBUG", "0") == "1"
    ASSETS_AUTO_BUILD = True

    # Development Feature Flags settings
    FEATURE_NEW_UI = True
    FEATURE_BETA = True
    FEATURE_PREMIUM = False
