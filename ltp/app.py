import logging.config

from flask import Flask, Blueprint

# Local imports
import settings
from api.restplus import api
from api.healthcheck import ns as healthcheck_namespace

app = Flask(__name__)
logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(healthcheck_namespace)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

def main():
    initialize_app(app)
    log.info('>>> Starting development server at http://{}/api/'.format(app.config['SERVER_NAME']))
    app.run(debug=True)

if __name__ == "__main__":
    main()

