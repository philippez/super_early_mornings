from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectField, DateField, IntegerField
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
    asset_currency = StringField('Asset_Currency', validators=[DataRequired()])
    asset_region = StringField('Asset_Region', validators=[DataRequired()])
    asset_type = StringField('Asset_Type', validators=[DataRequired()])
    super_theme = SelectField('Super_Theme', coerce=int, validators=[DataRequired()])
    micro_theme = StringField('Micro_Theme', validators=[DataRequired()])
    bloomberg_ticker = StringField('BB_Ticker', validators=[DataRequired()])
    sec_ref = StringField('Sec_Ref', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterSuperThemeForm(FlaskForm):
    super_theme_name = StringField('Super Theme Name', validators=[DataRequired()])
    super_theme_desc = TextAreaField('Super Theme Description', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

class RegisterTxTypeForm(FlaskForm):
    tx_type_name = StringField('Tx Type Name', validators=[DataRequired()])
    tx_type_desc = TextAreaField('Tx Type Description', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

class RegisterTransactionForm(FlaskForm):
    transaction_date = DateField('Transaction Date', validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', coerce=int, validators=[DataRequired()])
    transaction_qty = IntegerField('Quantity', validators=[DataRequired()])
    transaction_price = IntegerField('Price', validators=[DataRequired()])
    transaction_asset = SelectField('Asset', coerce=int, validators=[DataRequired()])
    transaction_platform = SelectField('Platform', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterPlatformForm(FlaskForm):
    platform_name = StringField('Platform Name', validators=[DataRequired()])
    platform_desc = TextAreaField('Platform Description', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

class AssetPriceForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    asset = SelectField('Asset', coerce=int, validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')



class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class TestForm(FlaskForm):
    a = [1,2,3,4]
    for i in range(5):
        field_x = SelectField('Number', choices = a)
        i =+ 1
    submit = SubmitField('Submit')