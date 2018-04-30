from flask_restplus import fields
from .restplus import api

from ..database.models import Activity

item_request = api.model('Item_Request', {
    'item': fields.Raw(required=False,
                       description='A collection of items')
})

item_collection = api.model('item_collection', {
    'items': fields.Raw(required=True,
                        description='A collection of items')
})

activity_request = api.model('Activity_Request', {
    'description': fields.String(required=False,
                                 description='Unique identifier for activity'),
})

activity_response = api.inherit('Activity_Response', activity_request, {
    'context': fields.String(attribute='@context'),
    'url': fields.String(attribute='@id',
                         description='Unique URL for the activity'),
    'created_time': fields.DateTime(),
    'hasItems': fields.List(fields.String, attribute='hasItem', required=False)
})


blob = api.model('Blob', {
    'id': fields.Integer(readOnly=True,
                         descrption='Unique identifier for the blob'),
    'content_type': fields.String(required=True,
                                  description='Content-Type of item'),
    'content_length': fields.Integer(required=True,
                                     description='Length of item, in bytes'),
    'content_hash': fields.String(required=True,
                                  description='ex: sha256:<hash of object>'),
    'created_at': fields.DateTime(readOnly=True),
})
