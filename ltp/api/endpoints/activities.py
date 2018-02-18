import logging
log = logging.getLogger(__name__)

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ..restplus import api
from ..serializers import activity
from ...database.models import Activity

ns = api.namespace('activities', description='Groups related items')

@ns.route('/')
class ActivityCollection(Resource):

    @api.expect(activity, validate=True)
    @api.response(201, 'Activity created')
    @api.marshal_with(activity)
    def post(self):
        """
        Creates a new activity containing one or more items
        """
        data = request.json
        try:
            activity = Activity(**data)
        except TypeError:
            raise BadRequest("Invalid JSON payload: {}".format(request.json))

        return activity, 201

