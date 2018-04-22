import logging.config

import click
from click import Abort, echo, confirm, style
from flask import Flask, Blueprint, got_request_exception, current_app
from flask.cli import with_appcontext
import pdb
from rdflib import ConjunctiveGraph, Graph, URIRef
import subprocess
import sys
import traceback


# Local imports
from .api.restplus import api
from .api.endpoints.healthcheck import ns as healthcheck_namespace
from .api.endpoints.activities import ns as activities_namespace
from .api.endpoints.blobs import ns as blobs_namespace
from .api.endpoints.items import ns as items_namespace
from .database import get_db, setup_db
from .settings import Config

logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)


def create_app(name=__name__, config=None, skip_defaults=False):
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

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api.add_namespace(healthcheck_namespace)
    api.add_namespace(activities_namespace)
    api.add_namespace(blobs_namespace)
    api.add_namespace(items_namespace)
    init_app(app)
    api.init_app(blueprint)

    blueprint.before_request(setup_db)
    app.register_blueprint(blueprint)

    got_request_exception.connect(drop_into_pdb)
    try:
        if '-echo' in str(subprocess.check_output("stty", shell=True)):
            log.debug("Re-enabling echo w/ stty")
            subprocess.check_call("stty echo", shell=True)
    except subprocess.CalledProcessError:
        pass

    return app


def drop_into_pdb(app, exception):
    """
    https://gist.github.com/alonho/4389137
    """
    traceback.print_exc()
    pdb.post_mortem(sys.exc_info()[2])


@click.command('initdb')
@click.option('--yes', is_flag=True)
@click.option('--load_examples', is_flag=True)
@with_appcontext
def init_db_command(yes=False, load_examples=False):
    """
    Wipe DB and populate with default entries
    """
    did_confirm = yes

    # Abort if we're using in-memory DB
    db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', None)
    if not db_uri or ':memory:' in db_uri:
        echo(style("initdb doesn't make sense with an in-memory DB", bg='red'))
        raise Abort()

    echo('---')
    msg = style("WIPE database, destroying ALL data?", bg='red')
    if not did_confirm and not confirm(msg):
        raise Abort()

    with current_app.open_resource('database/schema.json') as f:
        log.warning("Initializing database...")

        db = get_db()
        log.debug("Using {} as database.".format(str(db.store.engine)))
        db.store.destroy(db.store.engine)
        db.close()

        db = get_db()
        data = f.read()
        db.parse(data=data, format='json-ld')
        db.store.commit()
        log.info(f"Graph initialized from {f.name} with {len(db)} triples.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)

