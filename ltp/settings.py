class BaseConfig(object):
    # Flask settings
    SERVER_NAME = 'localhost:8888'
    DEBUG = True  # Do not use debug mode in production
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

class TestConfig(object):
    # Flask settings
    SERVER_NAME = 'localhost:8888'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Allow exceptions to propogate to the test client (vs 500 errors)
    TESTING = True

    # Enable in-page debugger
    DEBUG = True

