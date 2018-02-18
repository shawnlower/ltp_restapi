class BaseConfig(object):
    # Flask settings
    SERVER_NAME = 'localhost:8888'
    DEBUG = True  # Do not use debug mode in production
    TESTING = True

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
