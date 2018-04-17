"""
Database setup routines

rdflib-sqlalchemy provides the persistence layer for rdflib

"""

from flask import current_app as app, g
import logging
import rdflib
from rdflib import plugin, Literal, URIRef
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.plugin import Parser, Store, register

import socket

log = logging.getLogger(__name__)


def setup_db():
    """
    Perform initial setup routines.
    """
    log.debug("*** Running DB setup")
    g.graph = get_db()


def get_db():

    graph = getattr(g, 'graph', None)
    if graph:
        return graph

    register('SQLAlchemy', Store, 'rdflib_sqlalchemy.store', 'SQLAlchemy')
    register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')

    ident = URIRef("rdflib_test")

    store = plugin.get("SQLAlchemy", Store)(identifier=ident)
    graph = rdflib.ConjunctiveGraph(store, identifier=ident)

    uri_string = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')
    uri = Literal(f"{uri_string}")

    graph.open(uri, create=app.config['SQLALCHEMY_CREATE_DB'])
    graph.store.create_all()
    log.debug("Created graph {} with store {} ({})".format(id(graph),
              id(graph.store), repr(graph.store)))



    # Setup namespace
    ns_uri = app.config.get('LTP_NS_URI')
    if not ns_uri:
        ns_uri = 'http://{}/{}/'.format(
            app.config.get('SERVER_NAME'), '/api/items')
        app.config['LTP_NS_URI'] = ns_uri

    ns_prefix = app.config.get('LTP_NS_PREFIX', 'ltp')
    if not ns_prefix:
        ns_prefix = 'ltp'
        app.config['LTP_NS_PREFIX'] = 'ltp'

    g_namespaces = [ns for (ns, _) in graph.namespace_manager.namespaces()]
    if ns_prefix not in g_namespaces:
        ns = Namespace(ns_uri)
        ns_manager = NamespaceManager(graph)
        ns_manager.bind(ns_prefix, ns)

    return graph

