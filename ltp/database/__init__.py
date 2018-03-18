"""
Database setup routines

rdflib-sqlalchemy provides the persistence layer for rdflib

"""

from flask import current_app as app
import logging
import rdflib
from rdflib import plugin, Literal, URIRef
from rdflib.plugin import Parser, Store, register

log = logging.getLogger(__name__)


def get_graph(app, ident='rdflib'):
    ident = URIRef("rdflib_test")
    uri_string = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')
    uri = Literal(f"{uri_string}")

    register('SQLAlchemy', Store, 'rdflib_sqlalchemy.store', 'SQLAlchemy')
    register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
    store = plugin.get("SQLAlchemy", Store)(identifier=ident)
    graph = rdflib.Graph(store, identifier=ident)
    graph.open(uri, create=app.config['SQLALCHEMY_CREATE_DB'])
    log.debug("Created graph {} with store {} ({})".format(id(graph),
              id(graph.store), repr(graph.store)))
    return graph


def setup_db():
    """
    Perform initial setup routines.
    """

    # Ensure that we only call this once
    if hasattr(app.config.graph.store, '_setup_complete'):
        return
    setattr(app.config.graph.store, '_setup_complete', True)
    log.debug("*** Running DB setup")
    app.config.graph.store.create_all()

