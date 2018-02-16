import logging
log = logging.getLogger(__name__)

from flask_restplus import Api

from ltp import settings

api = Api(version='1.0', title='LTP API',
            description='Flask-restplus powered API server for LTP')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception has occurred ({})'.format(e)
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
