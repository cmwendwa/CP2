import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://mimi:mimi123@localhost/bucketist'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):

    SQLALCHEMY_TRACK_MODIFICATIONS = True
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
    'SECRET_KEY': '1Jclemn',
}
