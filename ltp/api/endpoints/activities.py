import logging
log = logging.getLogger(__name__)

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ..restplus import api
from ..serializers import activity
from ...database.models import db, Activity, Item

ns = api.namespace('activities', description='Groups related items')

@ns.route('/')
class ActivityCollection(Resource):

    @api.expect(activity, validate=False)
    @api.response(201, 'Activity created')
    @api.marshal_with(activity, envelope='activity')
    def post(self):
        """
        Creates a new activity containing one or more items
        """
        data = request.json
        if not data.get('items'):
            raise BadRequest("Payload validation failed. 'items' is empty: {}".format(data))
        try:
            activity_res = Activity(data)
            for item in data['items']:
                item_res = Item(item)
                log.debug(item_res)
                db.session.add(item_res)
        except TypeError as e:
            log.debug("validation failed: payload: {} \n error: {}".format(data,e))
            raise BadRequest("payload validation failed: {}".format(data))
        db.session.add(activity_res)
        db.session.commit()

        return activity_res, 201

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


