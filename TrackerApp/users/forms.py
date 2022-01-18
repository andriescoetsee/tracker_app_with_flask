from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

from flask_login import current_user
from TrackerApp.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first() is None:
            flash("Sorry, your username does not exist please register first!")
            raise ValidationError('Sorry, your username does not exist please register first!')

class RegistrationForm(FlaskForm):
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')
    
    def validate_password(self,field):
        if field.data != self.pass_confirm.data:
             flash("Sorry, passwords must match!")
             raise ValidationError('Passwords must match!')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            flash("Sorry, your username has been registered already!")
            raise ValidationError('Your username has been registered already!')
    