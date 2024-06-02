import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    DEVELOPMEN = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'assethub.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'test.db')
    TESTING = True
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class ProductionConfig:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'postgresql://otoolee101:j6tcxzxYpBjfNsul66quUX6QaTqYYWFp@dpg-cngfn7v79t8c73839qr0-a/postgresql_booker_assignment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #postgressql://otoolee101:j6tcxzxYpBjfNsul66quUX6QaTqYYWFp@dpg-cngfn7v79t8c73839qr0-a/postgresql_booker_assignment