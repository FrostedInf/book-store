import os
from werkzeug.utils import secure_filename

class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelomentConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/libros2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/img/books'
