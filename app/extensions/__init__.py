# app/extensions/__init__.py
from app.extensions.db import db
from app.extensions.login import login_manager, init_login_manager
from app.extensions.assets import assets
from app.extensions.cache import cache, init_cache
from app.extensions.mail import mail, init_mail
from app.extensions.limiter import limiter

from flask_migrate import Migrate

migrate = Migrate()

__all__ = [
    'db',
    'login_manager', 'init_login_manager',
    'assets',
    'cache', 'init_cache',
    'mail', 'init_mail',
    'limiter'
]
