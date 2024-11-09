from flask_mail import Message
from app.core.extensions import mail
from flask import current_app, render_template

def send_email(subject, recipients, template, **kwargs):
    """Send an email using templates."""
    msg = Message(
        subject=subject,
        recipients=recipients,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = render_template(f'email/{template}.txt', **kwargs)
    msg.html = render_template(f'email/{template}.html', **kwargs)
    
    mail.send(msg)