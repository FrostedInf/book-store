from flask_sqlalchemy import SQLAlchemy
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
    password = db.Column(db.String(66))
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def verify_password(self, password):
        return self.password == password

class Books(db.Model):
    __tablename__= 'libros'
    ISBN = db.Column(db.String(30), primary_key=True)
    titulo = db.Column(db.String(50))
    vecesVendido = db.Column(db.Integer)
    numeroPaginas = db.Column(db.Integer)
    existencia = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    editorial = db.Column(db.String(50))
    fechaPublicacion = db.Column(db.Date)
    precio = db.Column(db.Float)
    autor = db.Column(db.String(50))
    portada = db.Column(db.Text)
    libroCliente_id = db.relationship('LibroCliente')

class Compra(db.Model):
    __tablename__= 'compra'
    id = db.Column(db.Integer, primary_key=True)
    RFC = db.Column(db.String(50), primary_key=True)
    monto = db.Column(db.Float)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    libroCliente_id = db.relationship('LibroCliente')
    created_date_compra = db.Column(db.DateTime, default = datetime.datetime.now)

class LibroCliente(db.Model):
        __tablename__ = 'libroCliente'
        id = db.Column(db.Integer, primary_key=True)
        id_compra = db.Column(db.Integer, db.ForeignKey('compra.id'))
        id_libro = db.Column(db.String(30), db.ForeignKey('libros.ISBN'))
        id_usuario = db.Column(db.Integer, db.ForeignKey('users.id'))
        cantidad = db.Column(db.Float)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(66))
