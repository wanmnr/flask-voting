from flask import Blueprint, render_template

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/profile')
def profile():
    return render_template('')

@users_bp.route('/settings')
def settings():
    return render_template('')