# app/extensions/security.py
from flask_security import Security, SQLAlchemyUserDatastore
from .db import db
from app.models.user import User, Role

# Initialize extensions
security = Security()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def init_security(app):
    security.init_app(app, user_datastore)
