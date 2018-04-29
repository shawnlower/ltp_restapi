from flask_restplus import fields
from .restplus import api

from ..database.models import Activity

item = api.model('Item', {
    '@context': fields.String(required=True,
                              description='JSON-LD context for the item.'),
    '@type': fields.String(required=True,
                           description='JSON-LD type for the item.')
})

item_collection = api.model('Item_collection', {
    'items': fields.Raw(required=True,
                        description='A collection of items')
})

item_response = api.model('Item', {
    'id': fields.String(required=True, description='ID of new item'),
    'item': fields.Raw()
})

activity_request = api.model('Activity_Request', {
    'description': fields.String(required=False,
                                 description='Unique identifier for activity'),
})

activity_response = api.inherit('Activity_Response', activity_request, {
    'url': fields.String(attribute='@id',
                         description='Unique URL for the activity'),
    'created_time': fields.DateTime(),
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
