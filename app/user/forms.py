from flask import flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.extensions import *
from app.models.models import User, Branch


def validate_password_strength(form, field):
    password = field.data
    if any(c.isupper() for c in password) and \
       any(c.islower() for c in password) and \
       any(c.isdigit() for c in password) and \
       any(not c.isalnum() for c in password):
        pass
    else:
        flash ('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
        raise ValidationError('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')

"""class to register form ensuring username and password meets requirements"""
from wtforms import SelectField

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20), validate_password_strength], render_kw={"placeholder": "Password"})
    branch_name = SelectField('Branch Name', coerce=int)
    submit = SubmitField('Register')

    """check username is unique"""
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash("User already exists")
            raise ValidationError('That username already exists. Please choose a different one.')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [(0, 'Select Branch')] + [(branch.branch_id, branch.branch_name) for branch in Branch.query.all()]
        self.branch_name.render_kw = {"placeholder": "Select Branch"}


            
"""class to log into making sure it meets validation requirements"""
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
