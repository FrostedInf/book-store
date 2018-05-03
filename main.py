from flask import Flask
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
from flask_wtf import CSRFProtect
from config import DevelomentConfig
import forms

app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_ver():
        g.conectado = False
        if 'username' in session:
            g.conectado = True
        if 'username' not in session and request.endpoint in ['perfil', 'carrito', 'tienda']:
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

@app.route("/busqueda")
def busqueda():
	return render_template('busqueda.html', conectado = g.conectado)

@app.route("/tienda")
def tienda():
    return render_template('tienda.html', conectado = g.conectado)

@app.route("/carrito")
def carrito():
    return render_template('carrito.html', conectado = g.conectado)

@app.route("/perfil")
def perfil():
    return render_template('perfil.html', conectado = g.conectado)

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
# Admin Controllers
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('admin_views/admin_home.html', conectado = g.conectado)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
