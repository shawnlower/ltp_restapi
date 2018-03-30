from flask import abort, current_app as app, request, g
from flask_restplus import Resource
from rdflib import Graph, RDF
from rdflib.namespace import Namespace
from rdflib.term import BNode

from ..restplus import api
from ..serializers import item, item_collection, item_response
from ...utils.debug_requests import debug_requests
from ...utils import find_existing
from ...database import get_db

from hashlib import sha256
import json
import logging

log = logging.getLogger(__name__)

ns = api.namespace('items', description='Items representing semantic data')


@ns.route('/')
class ItemCollection(Resource):

    @api.expect(item, validate=True)
    @api.response(201, 'Item created')
    @api.marshal_with(item_response)
    def post(self):
        """
        Creates a new item
        """

        # Create a temporary graph to store the item
        tmp_g = Graph()

        doc = request.json

        # Ensure we DO NOT have 'id' set.
        # Providing an ID within the document might have a use case, e.g.
        # cache the item locally, but preserve the source link
        if 'id' in doc:
            return 409,\
                "Invalid request: Providing 'id' is not /yet/ supported."

        # Create an ID, based on the hash of the document
        hash = sha256(json.dumps(doc).encode()).hexdigest()
        id = app.config.get('LTP_NS_URI') + hash
        doc['@id'] = id

        # Populate the temporary graph with our document
        data = json.dumps(doc)
        with debug_requests():
            tmp_g.parse(data=data, format='application/ld+json')

        # Look for any existing match
        (subject, r_type) = list(tmp_g.subject_objects(RDF['type']))[0]
        if subject in g.graph.subjects():
            abort(409, "Conflict: exact match already exists: {}".format(
                  subject))
        existing = find_existing(tmp_g, subject, r_type, g.graph)
        if existing:
            abort(409, "Conflict: {} matches {}".format(
                  subject, existing))

        for t in tmp_g:
            g.graph.add(t)
        log.debug("Added {} to store (total size {})".format(
                  len(tmp_g), len(g.graph)))

        return {'id': hash, 'item': data}, 201

    @api.marshal_with(item_collection)
    @api.response(200, 'Ok')
    def get(self):
        """
        Retrieve a list of items
        """
        log.debug("found graph {} with store {} and size {}".format(
                  id(g.graph), id(g.graph.store), str(len(g.graph))))
        data = json.loads(g.graph.serialize(format='json-ld',
                          auto_compact=True))
        return {'items': data}


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
        ns = Namespace(app.config.get('LTP_NS_URI'))
        subject = ns[id]  
        g_item = Graph()
        g_item += g.graph.triples((subject, None, None))

        if not g_item:
            abort(404, "Item not found: {}".format(id))

        doc = g_item.serialize(format='json-ld', auto_compact=True)\
                .decode('utf-8')
        data = json.loads(doc)

        return {'id': id, 'item': data}, 200


