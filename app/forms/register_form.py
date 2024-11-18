# app/forms/register_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=255)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=50)
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
