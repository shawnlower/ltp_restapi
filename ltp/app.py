import logging.config
import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

# Local imports
from .api.restplus import api
from .api.endpoints.healthcheck import ns as healthcheck_namespace
from .api.endpoints.activities import ns as activities_namespace
from .api.endpoints.blobs import ns as blobs_namespace
from .api.endpoints.items import ns as items_namespace
from .database.models import db
from .database import setup_db
from .settings import Config

logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)

def create_app(name, config=None, skip_defaults=False):
    """
    app factory
    If config is not passed, env is inspected for 'APP_CONFIG'. If not present,
    the base defaults from settings.BaseConfig apply (local server, etc)
    """

    app = Flask(name)
    if not config:
        log.warning("Using default config")
        config = Config()
    app.config.from_object(config)

    with app.app_context():
        # Initialize our DB object with the engine configured for the app
        db.init_app(app)
        # Perform any setup necessary (create tables, etc)
        setup_db()

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(healthcheck_namespace)
    api.add_namespace(activities_namespace)
    api.add_namespace(blobs_namespace)
    api.add_namespace(items_namespace)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    return app

