# app/views/auth.py

from flask import Blueprint, current_app, render_template, redirect, session, url_for, flash, request
from urllib.parse import urlparse
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed
from app.extensions.mail import send_email
from app.extensions.limiter import limiter
from app.extensions.db import db
from app.models.user import User
from app.services.auth.auth_service import AuthenticationService
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Create an instance of AuthenticationService
        auth_service = AuthenticationService()
        success, user, message = auth_service.validate_login(
            form.username.data,
            form.password.data
        )

        if success:
            # Login user and start session
            login_user(user, remember=form.remember_me.data)
            session.permanent = True  # Make session permanent if remember me is checked

            # Set up user identity for Flask-Principal
            identity_changed.send(current_app._get_current_object(),
                               identity=Identity(user.id))

            flash('Successfully logged in!', 'success')

            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)

        flash(message, 'error')

    return render_template('auth/login.html', form=form)



@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        auth_service = AuthenticationService()
        success, message, user = auth_service.register_user({
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data
        })

        if success and user:
            login_user(user)  # Auto-login after registration
            flash('Registration successful! Welcome!', 'success')
            return redirect(url_for('main.home'))

        flash(message, 'error')

    return render_template('auth/register.html', form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    # Clear session
    session.clear()

    # Logout user
    logout_user()

    # Remove user identity for Flask-Principal
    identity_changed.send(current_app._get_current_object(),
                        identity=AnonymousIdentity())

    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def forgot_password():
    return render_template('auth/forgot_password.html')
