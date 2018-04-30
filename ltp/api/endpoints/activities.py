from datetime import datetime
from flask import abort, current_app as app, request, g
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ...database.models import Activity
from ..restplus import api
from ..serializers import activity_request, activity_response

import logging
log = logging.getLogger(__name__)

ns = api.namespace('activities', description='Groups related items')


@ns.route('/')
class ActivityCollection(Resource):

    @api.expect(activity_request)
    @api.marshal_with(activity_response)
    @api.response(201, 'Activity created')
    def post(self):
        """
        Creates a new activity
        """
        data = request.json

        now = datetime.utcnow().isoformat()
        data['created_time'] = now

        # Our type is already registered within the DB, so generate a
        # model object that looks like what we'll be interacting with
        try:
            activity = Activity(data)
        except KeyError:
            raise BadRequest("payload validation failed: {}".format(data))

        activity.save()
        log.debug("Wrote activity: " + str(activity._to_dict()))
        return activity._to_dict(), 201

    @api.marshal_list_with(activity_response, envelope='activities')
    @api.response(200, 'Ok')
    def get(self):
        """
        Retrieve a list of activities
        """
        return [a._to_dict() for a in Activity().get_all()]


@ns.route('/<string:id>')
class ActivityResource(Resource):

    @api.marshal_with(activity_response)
    @api.response(200, 'Ok')
    @api.response(404, 'Activity not found')
    def get(self, id):
        """
        Retrieve a single activity
        """
        activity = Activity().get(id)
        if not activity:
            abort(404, "Activity not found")
        return activity

    @api.expect(activity_request)
    @api.marshal_with(activity_response)
    @api.response(200, 'Ok')
    @api.response(404, 'Activity not found')
    def put(self, id):
        """
        Update an activity, e.g. to add a new item
        """
        activity = Activity().get(id)
        if not activity:
            abort(404, "Activity not found")

        return activity._update(request.json)
