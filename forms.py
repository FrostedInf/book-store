from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms import validators

class LoginForm(Form):
    username =  StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])