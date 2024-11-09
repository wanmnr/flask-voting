# app/core/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
# from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
assets = Environment()
cache = Cache()
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    storage_options={
        "socket_connect_timeout": 30,
        "socket_timeout": 30
    },
    strategy="fixed-window"
)
jwt = JWTManager()
# socketio = SocketIO()
csrf = CSRFProtect()


# Combined assets.py
def init_assets(app):
    """Initialize and configure asset bundles"""
    assets = Environment(app)
    assets.debug = app.debug
    
    # Bundle definitions
    css = Bundle(
        'css/vendor/*.css',
        'css/main.css',
        'css/style.css',
        filters='cssmin',
        output='dist/css/main.min.css',
        depends='css/*.css'
    )

    # Define SCSS bundle
    scss = Bundle(
        'scss/sidebar.scss',
        filters='libsass',
        output='css/sidebar.css',
        depends=['scss/_variables.scss']
    )
    
    js = Bundle(
        'js/vendor/*.js',
        'js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )
    
    # Register bundles
    assets.register('css_all', css)
    assets.register('scss_all', scss)
    assets.register('js_all', js)
    
    return assets