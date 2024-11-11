# app/extensions/mail.py
from flask_mail import Mail, Message
from flask import current_app, render_template
from flask import Flask
from typing import List

mail = Mail()

def init_mail(app: Flask) -> None:
    """Initialize mail with custom handlers"""

    def send_async_email(msg: Message) -> None:
        with app.app_context():
            mail.send(msg)

    app.send_async_email = send_async_email
    mail.init_app(app)

def send_email(subject, recipients, template, **kwargs):
    """Send an email using templates."""
    msg = Message(
        subject=subject,
        recipients=recipients,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = render_template(f'email/welcome.txt', **kwargs)
    msg.html = render_template(f'email/welcome.html', **kwargs)

    mail.send(msg)


def send_password_reset_email(user, reset_token):
    msg = Message(
        "Password Reset Request",
        recipients=[user.email]
    )

    # Render both HTML and plain text versions
    msg.html = render_template('email/reset_password.html',
        user=user,
        reset_token=reset_token,
        app_name=app.config['APP_NAME'],
        expiration_time=24,  # or whatever your token expiration time is
        year=datetime.utcnow().year
    )
    msg.body = render_template('email/reset_password.txt',
        user=user,
        reset_token=reset_token,
        app_name=app.config['APP_NAME'],
        expiration_time=24,
        year=datetime.utcnow().year
    )

    mail.send(msg)
