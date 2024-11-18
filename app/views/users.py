from flask import Blueprint, render_template
from flask_login import login_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html')

@users_bp.route('/settings')
@login_required
def settings():
    return render_template('pages/settings.html')
