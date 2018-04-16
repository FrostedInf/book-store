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

if __name__ == '__main__':
    app.run(debug=True)