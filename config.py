import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'tripleX'
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + \
        os.path.join(basedir, 'data-store.sqlite')#os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {


    'Production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'SECRET_KEY':'1Jclemn',
}

