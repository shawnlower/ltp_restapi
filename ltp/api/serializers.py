from flask_restplus import fields

from api.restplus import api

activity = api.model('Activity', {
    'id': fields.Integer(readOnly=True, description='Unique identifier of the activity'),
    'description': fields.String(required=False, description='Unique identifier of the activity'),
    })


