# app/models/user.py
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timezone
from app.extensions.db import db

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Flask-User required fields
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True)  # Required by Flask-Security
    confirmed_at = db.Column(db.DateTime())

    # Profile fields
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # Additional fields
    created_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    last_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))

    # Relationships
    roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.roles:
            default_role = Role.query.filter_by(name='user').first()
            if default_role:
                self.roles.append(default_role)
