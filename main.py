from flask import Flask,json
from flask import render_template
from flask import make_response
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import g
from models import db
from models import User
from models import Books
from models import Compra
from models import Carrito
import os
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
from werkzeug.datastructures import CombinedMultiDict
from flask_wtf.file import FileField
from config import DevelomentConfig
import forms

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_ver():
        g.conectado = False
        if 'username' in session:
            g.conectado = True
        if 'username' not in session and request.endpoint in ['perfil', 'carrito', 'tienda', 'favouriteBooks', 'tienda']:
            return redirect(url_for('login'))

@app.after_request
def after_ver(response):
    return response

#User Controllers
@app.route('/')
def index():
    title = "Inicio"
    return render_template('index.html', title = title, conectado = g.conectado)

@app.route('/contact')
def contactView():
    return render_template('contact.html', conectado = g.conectado)

@app.route('/registro', methods = ['GET', 'POST'])
def register():
    form = forms.UserFormRegister(request.form)
    if request.method == 'POST' and form.validate():
        user = User( form.username.data,
        form.email.data,
        form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado en la base de datos')

    return render_template('registro.html' ,form = form)

@app.route("/busqueda", methods=['GET', 'POST'])
def busqueda():
    form = forms.busquedaForm(request.form)
    if request.method == 'POST' and form.validate():
        item = form.busqueda.data
        resultado = Books.query.filter(Books.titulo.startswith(item)).all()
        if len(resultado) > 0:
            return render_template('libros.html',resultado=resultado , form = form)
        else:
            return render_template('busqueda0.html', form = form)
    return render_template('busqueda.html', conectado = g.conectado, form = form,resultado=Books.query.all())

@app.route("/agregarCarrito" , methods=['POST'])
def agregarCarrito():
    username = session['username']
    if request.method == 'POST':
        print(username)
        solicitud=request.get_json(force=True)
        user = User.query.filter_by(username = username).first()
        carrito = Carrito( user.id, solicitud['idLibro']
        )
        db.session.add(carrito)
        db.session.commit()
        return request.method



@app.route("/tienda", methods = ['GET'])
def tienda():
    return render_template('tienda.html', conectado = g.conectado)

@app.route("/carrito", methods = ['GET'])
def carrito():
    compra_list = Carrito.query.join(Books).add_columns(Books.id, Books.titulo, Books.portada, Books.precio)
    totalPrice = 0
    for libros in compra_list:
        totalPrice += libros[1]
    return render_template('carrito.html', totalPrice=totalPrice, compra_list = compra_list, conectado = g.conectado)

@app.route("/perfil", methods = ['GET', 'POST'])
def perfil():
    us1=session['username']
    print(us1)
    form = forms.tarjetaForm(request.form) 
    form1 = forms.envioForm(request.form)
    us2=User.query.filter_by(username=us1).first()
    # cargar datos de formulario tarjeta
    form.tarjeta.data = us2.numTarjeta
    form.titular.data = us2.titular
    form.fecha.data = us2.fechaVencimiento
    form.cvc.data = us2.cvc     
    # cargar datos de formulario envio
    form1.pais.data = us2.pais
    form1.direccion.data =us2.direccion
    form1.cp.data =us2.cp
    form1.ciudad.data =us2.ciudad
    form1.estado.data =us2.estado
    form1.telefono.data =us2.telefono

    if request.method == 'POST' and form.validate():
        form2 = forms.tarjetaForm(request.form)
        us2.numTarjeta = form2.tarjeta.data
        us2.titular = form2.titular.data
        us2.fechaVencimiento = form2.fecha.data
        us2.cvc = form2.cvc.data     
        db.session.commit()
        flash('Usuario registrado en la base de datos')


    if request.method == 'POST' and form.validate():      
        form3 = forms.envioForm(request.form)
        us2.pais = form3.pais.data    
        us2.direccion = form3.direccion.data
        us2.cp = form3.cp.data
        us2.ciudad = form3.ciudad.data
        us2.estado = form3.estado.data
        us2.telefono = form3.telefono.data
        db.session.commit()
        flash('DATOS CAMBIADOS EN LA BASE DE DATOS')


    return render_template('perfil.html', conectado = g.conectado, form=form, form1=form1, us2=us2)


@app.route('/login', methods = ['GET', 'POST'] )
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            flash('Bienvenido {}'.format(username))
            session['username'] = login_form.username.data
            session['password'] = login_form.password.data
            return redirect(url_for('index'))
        else:
            flash('usuario no encontrado')
    return render_template('login.html', form = login_form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/libros_favoritos', methods = ['GET', 'POST'])
def favouriteBooks():
    return render_template('librosFavoritos.html', conectado = g.conectado)
# Admin Controllers
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('admin_views/admin_home.html',
    conectado = g.conectado, usuarios = User.query.all(), libros = Books.query.all()  )

@app.route('/admin/delete_users/<int:identificador>', methods = ['POST'])
def deleteUsers(identificador):
    user = User.query.filter_by(id = identificador).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/show_users/<int:identificador>', methods = ['GET'])
def showUsers(identificador):
    user = User.query.filter_by(id = identificador).first()
    jsonStr = json.dumps(user.toJSON())
    return jsonStr

@app.route('/admin/create', methods = ['GET','POST'])
def createBooks():
    form = forms.BookFormRegister(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and form.validate():
        f = form.imagen.data
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        otherpath = path.replace('static/','')
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        book = Books(
        form.titulo.data,
        form.editorial.data,
        form.numeroPaginas.data,
        form.genero.data,
        form.autor.data,
        form.precio.data,
        otherpath
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin_views/view_create_books.html', form = form)


@app.route('/admin/delete_books/<int:identificador>', methods = ['POST'])
def deleteBooks(identificador):
    if request.method == 'POST':
        book = Books.query.filter_by(id = identificador).first()
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin_views/view_create_books.html', form = form)

@app.route('/admin/show_book/<int:identificador>', methods = ['GET'])
def showBook(identificador):
    book = Books.query.filter_by(id = identificador).first()
    jsonStr = json.dumps(book.toJSON())
    return jsonStr  

@app.route('/admin/edit_book/<int:identificador>', methods = ['GET','POST'])
def editBook(identificador):
    book = Books.query.filter_by(id = identificador).first()
    form = forms.BookFormRegister(request.form)
    #cargar los datos en el formulario
    form.titulo.data = book.titulo
    form.editorial.data = book.editorial
    form.numeroPaginas.data = book.numeroPaginas
    form.genero.data = book.genero
    form.autor.data = book.autor
    form.precio.data = book.precio
    #Actuliza los datos en base
    if request.method == 'POST' and form.validate():
        form2 = forms.BookFormRegister(request.form)
        book.titulo = form2.titulo.data
        book.editorial = form2.editorial.data
        book.numeroPaginas = form2.numeroPaginas.data
        book.genero = form2.genero.data
        book.autor = form2.autor.data
        book.precio = form2.precio.data
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin_views/view_edit_books.html',form = form)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
