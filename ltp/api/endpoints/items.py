import logging
log = logging.getLogger(__name__)

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ..restplus import api
from ..serializers import item
from ...database.models import db, Item

ns = api.namespace('items', description='Items representing semantic data')


@ns.route('/')
class ItemCollection(Resource):

    @api.expect(item, validate=True)
    @api.response(201, 'Item created')
    @api.marshal_with(item, envelope="item")
    def post(self):
        """
        Creates a new item
        """
        data = request.json
        try:
            item_res = Item(data)
        except TypeError as e:
            log.debug(
                "validation failed: payload: {} \n error: {}".format(data, e))
            raise BadRequest("payload validation failed: {}".format(data))
        db.session.add(item_res)
        db.session.commit()

        return item_res, 201

    @api.response(200, 'Ok')
    @api.marshal_list_with(item, envelope="items")
    def get(self):
        """
        Retrieve a list of items
        """
        items = Item.query.all()
        return items


@ns.route('/<int:id>')
class ItemResource(Resource):

    @api.marshal_list_with(item, envelope="item")
    def get(self, id):
        """
        Retrieve a single item
        """
        item = Item.query.filter(Item.id == id).one()
        return item
