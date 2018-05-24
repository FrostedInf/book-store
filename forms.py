from wtforms import Form
from wtforms import StringField, PasswordField, IntegerField, FloatField, FileField
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

class BookFormRegister(Form):
    """docstring for BookFormRegister"""
    titulo =  StringField('titulo', [validators.DataRequired()])
    editorial = StringField('Editorial', [validators.DataRequired()])
    numeroPaginas = IntegerField('numero', [validators.DataRequired()])
    precio = FloatField('precio', [validators.DataRequired()])
    genero = StringField('genero', [validators.DataRequired()])
    autor = StringField('autor', [validators.DataRequired()])
    imagen = FileField()

class busquedaForm(Form):
    busqueda = StringField('busqueda')
  
class tarjetaForm(Form):
    tarjeta = StringField()
    titular = StringField()
    fecha = StringField()
    cvc = StringField()

class envioForm(Form):
    pais = StringField()
    direccion = StringField() 
    cp  = StringField()
    ciudad = StringField() 
    estado = StringField() 
    telefono  = StringField()
    