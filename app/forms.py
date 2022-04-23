from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class RegisterAssetForm(FlaskForm):
    asset_name = StringField('Asset_Name', validators=[DataRequired()])
    asset_desc = TextAreaField('Asset_Desc', validators=[Length(min=0, max=140)])
    asset_region = StringField('Asset_Region', validators=[DataRequired()])
    asset_type = StringField('Asset_Type', validators=[DataRequired()])
    super_theme = StringField('Super_Theme', validators=[DataRequired()])
    micro_theme = StringField('Micro_Theme', validators=[DataRequired()])
    bloomberg_ticker = StringField('BB_Ticker', validators=[DataRequired()])
    sec_ref = StringField('Sec_Ref', validators=[DataRequired()])
    asset_opinion = StringField('Asset_Opinion', validators=[DataRequired()])
    submit = SubmitField('Submit')
