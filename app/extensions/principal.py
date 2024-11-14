# app/extensions/principal.py
from flask_principal import Principal, Permission, RoleNeed

# Initialize principal extensions
principal = Principal()

# Create role-based permissions
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
