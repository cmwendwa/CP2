import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "clement"  # os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/bl'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {


    'Production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'SECRET_KEY': '1Jclemn',
}
