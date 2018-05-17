from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    imagen = db.Column(db.String(50))
    compra = db.relationship('Compra')
    librocliente = db.relationship('LibroCliente')
    email = db.Column(db.String(40))
    password = db.Column(db.String(100))
    numTarjeta = db.Column(db.String(40))
    titular = db.Column(db.String(40))
    fechaVencimiento = db.Column(db.Date)
    cvc = db.Column(db.String(40))
    pais = db.Column(db.String(40))
    direccion = db.Column(db.String(40))
    cp = db.Column(db.String(40))
    ciudad = db.Column(db.String(40))
    estado = db.Column(db.String(40))
    telefono = db.Column(db.String(40))
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.__create_password(password)

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Books(db.Model):
    __tablename__= 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    vecesVendido = db.Column(db.Integer)
    numeroPaginas = db.Column(db.Integer)
    existencia = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    editorial = db.Column(db.String(50))
    fechaPublicacion = db.Column(db.Date)
    precio = db.Column(db.Float)
    autor = db.Column(db.String(50))
    portada = db.Column(db.String(80))
    libroCliente_id = db.relationship('LibroCliente')

    def __init__(self, titulo, editorial,numeroPaginas, genero, autor, precio, portada):
        self.titulo = titulo
        self.editorial = editorial
        self.numeroPaginas = numeroPaginas
        self.genero = genero
        self.autor = autor
        self.precio = precio
        self.portada = portada

class Compra(db.Model):
    __tablename__= 'compra'
    id = db.Column(db.Integer, primary_key=True)
    RFC = db.Column(db.String(50), primary_key=True)
    monto = db.Column(db.Float)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    libroCliente_id = db.relationship('LibroCliente')
    envio_id = db.relationship('Envio')
    created_date_compra = db.Column(db.DateTime, default = datetime.datetime.now)

class LibroCliente(db.Model):
        __tablename__ = 'libroCliente'
        id = db.Column(db.Integer, primary_key=True)
        id_compra = db.Column(db.Integer, db.ForeignKey('compra.id'))
        id_libro = db.Column(db.Integer, db.ForeignKey('libros.id'))
        id_usuario = db.Column(db.Integer, db.ForeignKey('users.id'))
        cantidad = db.Column(db.Float)
        precio = db.Column(db.Float)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(66))

class Envio(db.Model):
    __tablename__ = 'envio'
    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(40))
    colonia = db.Column(db.String(40))
    direccion = db.Column(db.String(40))
    cp = db.Column(db.String(40))
    ciudad = db.Column(db.String(40))
    estado = db.Column(db.String(40))
    telefono = db.Column(db.String(40))
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'))
