from flask import abort, current_app as app, request, g
from flask_restplus import Resource
from rdflib import URIRef, Graph, RDF
from rdflib.namespace import Namespace
from rdflib.term import BNode
import uuid

from ..restplus import api
from ...utils.debug_requests import debug_requests
from ...utils import find_existing
from ...database import get_db, get_ns
from ..serializers import item_request

from hashlib import sha256
import json
import logging
import urllib

log = logging.getLogger(__name__)

ns = api.namespace('items', description='Items representing semantic data')


@ns.route('/')
class ItemCollection(Resource):

    @api.response(201, 'Item created')
    @api.response(406, 'Unacceptable JSON/JSON-LD content')
    @api.expect(item_request)
    def post(self):
        """
        Creates a new item
        The payload must consist of a JSON-LD document for a single entity.
            @graph is not permitted
        """

        doc = request.json

        # validation
        if '@graph' in doc:
            return 406,\
                "Invalid request: Providing 'graph' is not supported."

        # Create a temporary graph to store the item
        tmp_g = Graph()

        # Populate the temporary graph with our document
        data = json.dumps(doc)
        with debug_requests():
            try:
                tmp_g.parse(data=data, format='application/ld+json')
            # Catch everything (HTTPError, connrefused, urlerror, ....... )
            except Exception as e: 
                abort(502, "Unable to parse graph: {}".format(
                    getattr(e, 'msg', str(e))))

        if not list(tmp_g):
            abort(406, "Unable to parse JSON-LD from input: {request.json}")

        # We want our new entities to be resolvable, and thus need IDs.
        # While we could simply set the ID on the document, we want to be as
        # liberal as possible in accepting valid JSON-LD data, which may be
        # nested. Therefore, we'll just parse it all, and then re-map the
        # BNodes to URIRefs

        # Get all subject bnodes (there should never be *unique* object BNodes)
        bnodes = list(set(filter(lambda s: isinstance(s, BNode),
                      tmp_g.subjects())))

        # We'll keep track of differences with running DB as well
        graph = get_db()
        unique = False
        # Keep track of potential duplicates in DB
        node_matches = set()
        for node in bnodes:
            # Create an ID, based on the hash of the document
            uri = URIRef(get_ns() + 'items/' + str(uuid.uuid4()))
            log.debug(f"Using {uri} for resource ID")

            ###
            # Replace as subject
            ###
            for (s, p, o) in tmp_g.triples((node, None, None)):
                # We only need a single different triple to be unique
                # this logic might be refactored for unique-ifying
                # based on type, but this is what we'll use now
                if not isinstance(o, BNode):
                    node_matches.update(graph.subjects(predicate=p, object=o))

                if not node_matches:
                    unique = True

            ###
            # Replace as object
            ###
            for (s, p, o) in tmp_g.triples((None, None, node)):
                node_matches.update(graph.objects(subject=s, predicate=p))

                if not node_matches:
                    unique = True

            # Swap BNode for URIRef
            for (s, p, o) in tmp_g.triples((node, None, None)):
                log.debug("for subject")
                tmp_g.add((uri, p, o))
                tmp_g.remove((s, p, o))

            for (s, p, o) in tmp_g.triples((None, node, None)):
                log.debug("for predicate")
                tmp_g.add((s, uri, o))
                tmp_g.remove((s, p, o))

            for (s, p, o) in tmp_g.triples((None, None, node)):
                log.debug("for object")
                tmp_g.add((s, p, uri))
                tmp_g.remove((s, p, o))

        if not unique:
            abort(409,
                  f"Conflict: exact match(es) already exist: {node_matches}")

        count = len([graph.add(t) for t in tmp_g if t not in graph])
        log.debug("Added {} to store (total size {})".format(
                  count, len(g.graph)))

        json_data = tmp_g.serialize(format='json-ld', auto_compact=True)
        return {'item': json.loads(json_data)}, 201

    # @api.marshal_with(item_collection)
    @api.response(200, 'Ok')
    def get(self):
        """
        Retrieve a list of items
        """
        log.debug("found graph {} with store {} and size {}".format(
                  id(g.graph), id(g.graph.store), str(len(g.graph))))
        data = json.loads(g.graph.default_context.serialize(format='json-ld',
                          auto_compact=True))
        return {'items': data['@graph']}


@ns.route('/<string:id>')
@api.response(200, 'Ok')
@api.response(404, 'Item not found')
# @api.marshal_with(item_response)
class ItemResource(Resource):

    def get(self, id):
        """
        Retrieve a single item

        An 'item' is the subgraph of all nodes where the subject matches
        <prefix> + <id>

        Example:
        prefix: http://ltp.shawnlower.net/1.0/i/
        id: c867215a18c3cae

        Our subject becomes:
        rdflib.term.URIRef('http://ltp.shawnlower.net/1.0/i/c867215a18c3cae')
        """

        # Setup our namespace
        ns = get_ns()
        subject = ns['items/' + id]  
        g_item = Graph()
        g_item += g.graph.triples((subject, None, None))

        if not g_item:
            abort(404, "Item not found: {}".format(id))

        doc = json.loads(g_item.serialize(format='json-ld', auto_compact=True)
                         .decode('utf-8'))

        return doc, 200


