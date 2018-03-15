from flask import abort, current_app as app, request
from flask_restplus import Resource
from rdflib import Graph
from rdflib.term import BNode

from ..restplus import api
from ..serializers import item

import json
import logging

log = logging.getLogger(__name__)

ns = api.namespace('items', description='Items representing semantic data')


@ns.route('/')
class ItemCollection(Resource):

    @api.expect(item, validate=True)
    @api.response(201, 'Item created')
    #   @api.marshal_with(item, envelope="item")
    def post(self):
        """
        Creates a new item
        """

        data = request.json['data']

        g = app.config.graph

        data = json.dumps(request.json['data'])
        g.parse(data=data, format='application/ld+json')
        data = json.loads(g.serialize(format='json-ld', auto_compact=True))
        return data, 201

    @api.marshal_with(item)
    # @api.marshal_with(item)
    @api.response(200, 'Ok')
    def get(self):
        """
        Retrieve a list of items
        """
        g = app.config.graph
        log.debug("found g {} with store {} and size {}".format(id(g),
                  id(g.store), str(len(g))))
        data = json.loads(g.serialize(format='json-ld', auto_compact=True))
        return {'data': data}


@ns.route('/<string:id>')
@api.response(200, 'Ok')
@api.response(404, 'Item not found in graph')
class ItemResource(Resource):

    # @api.marshal_list_with(item, envelope="item")
    def get(self, id):
        """
        Retrieve a single item
        """
        g = app.config.graph
        bnode = BNode(id)
        if bnode not in g.subjects():
            abort(404)

        # Create a new graph to store the triples matching our subject
        ret_graph = Graph()
        ret_graph += g.triples((bnode, None, None))
        data = json.loads(ret_graph.serialize(format='json-ld', auto_compact=True))
        return data


