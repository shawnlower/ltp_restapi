import logging
log = logging.getLogger(__name__)

from ltp import app

if __name__ == '__main__':
    ltp_app = app.create_app()
    log.info('>>> Starting development server at http://{}/api/'.format(ltp_app.config['SERVER_NAME']))
    ltp_app.run()

