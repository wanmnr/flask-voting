# app/config/_default.py
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

from app.extensions import db

# env_path = Path('.') / '.env'
# load_dotenv(env_path)

class DefaultConfig:
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    ENV_FILE = ROOT_DIR / '.env'

    print(f"Looking for .env file at: {ENV_FILE}")
    print(f"File exists: {ENV_FILE.exists()}")

    # Load with debug=True to see what's being loaded
    load_dotenv(ENV_FILE, override=True, verbose=True)

    # Debug prints
    print("Current directory:", ROOT_DIR)

    def __init__(self):
        # Print all environment variables for debugging
        print("Current environment variables:")
        for key, value in os.environ.items():
            if key in ['DATABASE_URL', 'SECRET_KEY', 'API_KEY']:
                print(f"{key}: {value}")

    """Base configuration."""
    # Default settings that are common across all environments
    APP_NAME = "Voting System"
    TESTING = False

    # Default development settings (from .flaskenv)
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    DEVELOPMENT = os.getenv("FLASK_ENV", "production") == "development"


    # Database path in project root
    DB_PATH = ROOT_DIR / 'instance/app.db'

    # Default database settings (from .env)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default cache settings (from .env)
    CACHE_TYPE = os.getenv("CACHE_TYPE", "redis")
    CACHE_REDIS_URL = os.getenv('REDIS_URL', "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 300

    # Default session settings (from .env)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_TYPE = "redis" # Options: filesystem, redis, memcached, sqlalchemy
    SESSION_FILE_DIR = '/tmp/flask_session'  # For filesystem sessions
    SESSION_KEY_PREFIX = 'flask_session:'  # For redis/memcached
    SESSION_SQLALCHEMY = db  # For sqlalchemy sessions
    SESSION_SQLALCHEMY_TABLE = 'sessions'  # For sqlalchemy sessions

    # Default cookies settings (from .env)
    REMEMBER_COOKIE_DURATION = timedelta(days=14)  # For "remember me" functionality

    # Default security settings (from .env)
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Default security headers settings (from .env)
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }

    # Default File Upload settings (from .env)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

    # Default Celery settings (from .env)
    CELERY_BROKER_URL = os.getenv("REDIS_URL")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    # Default Mail settings (from .env)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") == "1"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Default Logging settings (from .env)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(os.getcwd(), 'instance', 'logs', 'app.log'))

    # Default API settings (from .env)
    API_TITLE = os.getenv("API_TITLE", "Voting System API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Default i18n / Internationalization & Localization settings (from .env)
    LANGUAGES = ["en", "es", "fr"]
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "UTC")

    # Default Rate Limiting settings (from .env)
    RATELIMIT_DEFAULT = "200 per day;50 per hour;1 per second"
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL")
    RATELIMIT_STRATEGY = "fixed-window"

    # Default WebSocket settings (from .env)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("REDIS_URL")

    # Default Feature Flags settings (from .env)
    FEATURE_FLAGS = {
        'ENABLE_REGISTRATION': os.getenv("ENABLE_REGISTRATION", "1") == "1",
        'ENABLE_OAUTH': os.getenv("ENABLE_OAUTH", "0") == "1",
        'ENABLE_2FA': os.getenv("ENABLE_2FA", "0") == "1",
        'ENABLE_FILE_UPLOAD': os.getenv("ENABLE_FILE_UPLOAD", "1") == "1",
    }

    # Flask-Security configuration
    SECURITY_PASSWORD_SALT = 'your-security-password-salt'
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_POST_LOGOUT_VIEW = '/admin'

    # Default Flask-Admin Interface settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # AdminLTE3 configuration
    FLASK_ADMIN_SWATCH = 'cosmo'
    ADMINLTE_THEME = True
    ADMINLTE_LEGACY_USER_MENU = False
    ADMINLTE_SEARCH_FORM = False

    # Default Debug Toolbar settings (from .flaskenv)
    DEBUG_TB_ENABLED = os.getenv("FLASK_ENV") == "development"
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Default Assets settings (from .flaskenv)
    ASSETS_DEBUG = os.getenv("ASSETS_DEBUG", "0") == "1"
    ASSETS_AUTO_BUILD = True
