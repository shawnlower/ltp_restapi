import logging.config
import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

# Local imports
import settings
from api.restplus import api
from api.endpoints.healthcheck import ns as healthcheck_namespace
from api.endpoints.activities import ns as activities_namespace
from database.models import db

logging.config.fileConfig('logging.cfg')
log = logging.getLogger(__name__)

def create_app(config=None, skip_defaults=False):
    """
    app factory
    If config is not passed, env is inspected for 'APP_CONFIG'. If not present,
    the base defaults from settings.BaseConfig apply (local server, etc)
    """

    app = Flask(__name__)
    if not skip_defaults:
        app.config.from_object('settings.BaseConfig')

    if config:
        app.config.from_object(config)
    elif 'APP_CONFIG' in os.environ:
        app.config.from_envvar('APP_CONFIG')

    db.init_app(app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(healthcheck_namespace)
    api.add_namespace(activities_namespace)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    return app

def main():
    app = create_app()
    log.info('>>> Starting development server at http://{}/api/'.format(app.config['SERVER_NAME']))
    app.run()

if __name__ == "__main__":
    main()

