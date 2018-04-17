from flask import abort, current_app as app, request, g
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ...database import get_db
from ...database.models import Activity
from ..restplus import api
from ..serializers import activity
from ...utils.graph import make_pyclass

import logging
log = logging.getLogger(__name__)

ns = api.namespace('activities', description='Groups related items')


@ns.route('/')
class ActivityCollection(Resource):

    @api.expect(activity)
    @api.response(201, 'Activity created')
    @api.marshal_with(activity)
    def post(self):
        """
        Creates a new activity containing one or more items
        """
        data = request.json

        # Our type is already registered within the DB, so generate a 
        # model object that looks like what we'll be interacting with
        activity = Activity(data)
        # raise BadRequest("payload validation failed: {}".format(data))

        return activity, 201

    @api.response(200, 'Ok')
    @api.marshal_list_with(activity, envelope="activities")
    def get(self):
        """
        Retrieve a list of activities
        """
        activities = Activity.query.all()
        return activities


@ns.route('/<int:id>')
class ActivityResource(Resource):

    @api.marshal_list_with(activity, envelope="activity")
    def get(self, id):
        """
        Retrieve a single activity
        """
        activity = Activity.query.filter(Activity.id == id).one()
        return activity
