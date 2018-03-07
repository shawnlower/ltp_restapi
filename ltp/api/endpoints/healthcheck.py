import logging
log = logging.getLogger(__name__)

from flask import request
from flask_restplus import Resource

from ..restplus import api

ns = api.namespace('healthcheck', description='Health check')


@ns.route('/')
class Healthcheck(Resource):
    def get(self):
        """
        Returns: {'status': 'ok'}
        """
        return {'status': 'ok'}, 200
