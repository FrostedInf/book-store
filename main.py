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
    pass

@app.after_request
def after_ver(response):
    return response

#User Controllers
@app.route('/')
def index():
    title = "Titulo"
    conectado = "No"
    if 'username' in session:
        username = session['username']
        conectado = "Yes"
        print (username)
        print (conectado)
    return render_template('index.html', title = title, conectado = conectado)

@app.route('/contact')
def header():
    return render_template('contact.html')

@app.route("/busqueda")
def fn():
	return render_template('busqueda.html')
	
@app.route("/tienda")
def tienda():
    return render_template('tienda.html')

@app.route("/carrito")
def carrito():
    return render_template('carrito.html')

@app.route("/perfil")
def perfil():
    return render_template('perfil.html')
    
@app.route('/login', methods = ['GET', 'POST'] )
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        flash('Bienvenido {}'.format(username))
        session['username'] = login_form.username.data
        session['password'] = login_form.password.data
    return render_template('login.html', form = login_form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))
# Admin Controllers
@app.route('/admin_home')
def adminHomeView():
    return render_template('admin_views/admin_home.html')

@app.route('/consultar_stock')
def stockView():
    return render_template('admin_views/consultar_stock.html')

@app.route('/consultar_stock')
def stockView():
    return render_template('admin_views/consultar_stock.html')

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()