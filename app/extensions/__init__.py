# app/extensions/__init__.py
from app.extensions.db import db, init_db
from app.extensions.login import login_manager, init_login_manager
from app.extensions.assets import assets, init_assets
from app.extensions.cache import cache, init_cache
from app.extensions.mail import mail, init_mail
from app.extensions.limiter import limiter

__all__ = [
    'db', 'init_db',
    'login_manager', 'init_login_manager',
    'assets', 'init_assets',
    'cache', 'init_cache',
    'mail', 'init_mail',
    'limiter'
]
