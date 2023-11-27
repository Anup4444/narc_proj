import os
SECRET_KEY = 'mysecret'
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL') or 'mysql+mysqlconnector://root:root@localhost/my_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')


class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'narcgov1991@gmail.com'
    MAIL_PASSWORD = 'hxcg tffm daoy ijwu'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
