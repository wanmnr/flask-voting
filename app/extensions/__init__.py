# app/extensions/__init__.py
from app.extensions.admin import admin, init_admin
from app.extensions.adminlte3 import adminlte3
from app.extensions.assets import assets
from app.extensions.babel import babel
from app.extensions.cache import cache, init_cache
from app.extensions.db import db
from app.extensions.jwt import jwt, init_jwt
from app.extensions.limiter import limiter
from app.extensions.login import login_manager
from app.extensions.mail import mail, init_mail
from app.extensions.principal import principal
from app.extensions.security import security, init_security

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

marshmallow = Marshmallow()
migrate = Migrate()

__all__ = [
    'admin', 'init_admin',
    'adminlte3',
    'assets',
    'babel',
    'cache', 'init_cache',
    'db',
    'jwt', 'init_jwt',
    'limiter',
    'login_manager', 'init_login_manager',
    'mail', 'init_mail',
    'principal',
    'security', 'init_security',
]
