from flask_restplus import fields

from .restplus import api

item = api.model('Item', {
    '@context': fields.String(required=True,
                              description='JSON-LD context for the item.'),
    '@type': fields.String(required=True,
                           description='JSON-LD type for the item.')
})

item_collection = api.model('item_collection', {
    'items': fields.Raw(required=True,
                        description='A collection of items')
})

item_response = api.model('Item', {
    'id': fields.String(required=True, description='ID of new item'),
    'item': fields.Raw()
})


activity = api.model('Activity', {
    'id': fields.Integer(readOnly=True,
                         description='Unique identifier for the activity'),
    'description': fields.String(required=False,
                                 description='Unique identifier for activity'),
    'created_at': fields.DateTime(readOnly=True),
    'items': fields.List(fields.Nested(item)),
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
