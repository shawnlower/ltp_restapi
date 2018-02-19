import logging.config
import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

# Local imports
from . import settings
from .api.restplus import api
from .api.endpoints.healthcheck import ns as healthcheck_namespace
from .api.endpoints.activities import ns as activities_namespace
from .database.models import db
from .database import setup_db

logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)

def create_app(name, config=None, skip_defaults=False):
    """
    app factory
    If config is not passed, env is inspected for 'APP_CONFIG'. If not present,
    the base defaults from settings.BaseConfig apply (local server, etc)
    """

    app = Flask(name)
    if not skip_defaults:
        app.config.from_object(settings.BaseConfig())

    if config:
        app.config.from_object(config)
    elif 'APP_CONFIG' in os.environ:
        app.config.from_envvar('APP_CONFIG')

    with app.app_context():
        # Initialize our DB object with the engine configured for the app
        db.init_app(app)
        # Perform any setup necessary (create tables, etc)
        setup_db()

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(healthcheck_namespace)
    api.add_namespace(activities_namespace)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    return app

