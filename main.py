from flask import Flask
from flask import render_template
from flask import make_response
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/contact")
def header():
    return render_template('contact.html')

@app.route("/tienda")
def tienda():
    return render_template('tienda.html')

@app.route("/carrito")
def carrito():
    return render_template('carrito.html')

@app.route("/perfil")
def perfil():
    return render_template('perfil.html')
    
if __name__ == '__main__':
    app.run(debug=True)