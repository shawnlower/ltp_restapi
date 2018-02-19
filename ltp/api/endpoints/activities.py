import logging
log = logging.getLogger(__name__)

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from ..restplus import api
from ..serializers import activity
from ...database.models import db, Activity

ns = api.namespace('activities', description='Groups related items')

@ns.route('/')
class ActivityCollection(Resource):

    @api.expect(activity, validate=False)
    @api.response(201, 'Activity created')
    @api.marshal_with(activity)
    def post(self):
        """
        Creates a new activity containing one or more items
        """
        data = request.json
        try:
            activity_res = Activity(**data)
        except TypeError as e:
            log.debug("validation failed: payload: {} \n error: {}".format(data,e))
            raise BadRequest("payload validation failed: {}".format(data))
        db.session.add(activity_res)
        db.session.commit()

        return activity_res, 201

