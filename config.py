import os
class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelomentConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:filantro21@localhost/bookStore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False