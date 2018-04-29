from ..utils.graph import make_pyclass
from ..database import get_db, get_ns

import logging

logging.config.fileConfig('ltp/logging.cfg')
log = logging.getLogger(__name__)

# Define the models that we'll be using
# Since the models are based on semantic types that we have in the DB
# we've defined a helper factory method to generate classes based on
# their RDF Schema, hence the abuse of __new__


class Item():
    def __new__(self, *args, **kwargs):
        LTP = get_ns()
        return make_pyclass(LTP['Item'],
                            base=LTP + 'items',
                            graph=get_db())(*args, **kwargs)


class Activity():
    def __new__(self, *args, **kwargs):
        LTP = get_ns()
        return make_pyclass(LTP['Activity'],
                            base=LTP + 'activities',
                            graph=get_db())(*args, **kwargs)


class Blob():
    pass
#    created_at = db.Column(db.DateTime)
#    content_type = db.Column(db.String(100))
#    content_hash = db.Column(db.String(100))
#    content_length = db.Column(db.Integer)
#
#    def __init__(self, created_at, content_type, content_length,
#                 content_hash):
#        self.created_at = datetime.utcnow()
#        self.content_type = content_type
#        self.content_length = content_length
#        self.content_hash = content_hash
#
#    def __repr__(self):
#        return "<Blob {} (Size: {}, Type: {}) >".format((self.id,
#                                                         self.content_length,
#                                                         self.content_type))
