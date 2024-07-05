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
        or 'postgresql://major_project_database_2ech_user:rvDP9cS5v15s3jAE08CKKoet55JLlo9L@dpg-cq43uv5ds78s73ceoso0-a.oregon-postgres.render.com/major_project_database_2ech'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
