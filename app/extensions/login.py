# app/extensions/login.py

from flask_login import LoginManager

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Move the user loader function here
    @login_manager.user_loader
    def load_user(user_id):
        # Import User model locally to avoid circular imports
        from ..models.user import User
        return User.query.get(int(user_id))

