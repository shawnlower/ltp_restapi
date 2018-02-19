from flask_restplus import fields

from .restplus import api

item = api.model('Item', {
    'id': fields.Integer(readOnly=True, descrption='Unique identifier of the item'),
})

activity = api.model('Activity', {
    'id': fields.Integer(readOnly=True, description='Unique identifier of the activity'),
    'description': fields.String(required=False, description='Unique identifier of the activity'),
    'created_at': fields.DateTime(readOnly=True),
    'items': fields.List(fields.Nested(item)),
})
