# app/extensions/context_processor.py

from flask import request
from flask_login import current_user


def inject_user():
    """Inject user and other template variables into all templates."""
    return {
        'current_user': current_user,
        'request': request
    }
