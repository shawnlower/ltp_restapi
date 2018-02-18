import logging.config
import os

from flask import Flask, Blueprint

# Local imports
import settings
from api.restplus import api
from api.endpoints.healthcheck import ns as healthcheck_namespace
from api.endpoints.activities import ns as activities_namespace

logging.config.fileConfig('ltp/logging.cfg')

app = Flask(__name__)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    # Load base defaults
    flask_app.config.from_object('settings.BaseConfig')
    if 'APP_CONFIG' in os.environ:
        flask_app.config.from_envvar('APP_CONFIG')

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(healthcheck_namespace)
    api.add_namespace(activities_namespace)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

def main():
    initialize_app(app)
    log.info('>>> Starting development server at http://{}/api/'.format(app.config['SERVER_NAME']))
    app.run()

if __name__ == "__main__":
    main()

