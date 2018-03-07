from flask_restplus import fields

from .restplus import api

item = api.model('Item', {
    'id': fields.Integer(readOnly=True, descrption='Unique identifier of the item'),
    'content_type': fields.String(required=True, description='Content-Type of item'),
    'created_at': fields.DateTime(readOnly=True),
})

activity = api.model('Activity', {
    'id': fields.Integer(readOnly=True, description='Unique identifier of the activity'),
    'description': fields.String(required=False, description='Unique identifier of the activity'),
    'created_at': fields.DateTime(readOnly=True),
    'items': fields.List(fields.Nested(item)),
})

blob = api.model('Blob', {
    'id': fields.Integer(readOnly=True, descrption='Unique identifier of the blob'),
    'content_type': fields.String(required=True, description='Content-Type of item'),
    'content_length': fields.Integer(required=True, description='Length of item, in bytes'),
    'content_hash': fields.String(required=True, description='ex: sha256:<hash of object>'),
    'created_at': fields.DateTime(readOnly=True),
})
