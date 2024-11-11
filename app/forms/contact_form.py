# app/forms/contact_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    subject = SelectField('Subject', validators=[DataRequired()],
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Technical Support'),
            ('feedback', 'Feedback'),
            ('business', 'Business Proposal')
        ]
    )
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
