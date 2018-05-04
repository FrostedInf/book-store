from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms import validators
from models import User
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    username =  StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

class UserFormRegister(Form):
    username =  StringField('username', [validators.DataRequired(message = 'El username es requerido')])
    email = EmailField('email',
        [
        validators.DataRequired('El email es requerido'),
        validators.Email('Ingrese email valido')
        ])
    password = PasswordField('password', [validators.DataRequired(message = 'El password es requerido')])

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya se encuentra registrado')

class busquedaForm(Form):
    busqueda = StringField('busqueda')
        
