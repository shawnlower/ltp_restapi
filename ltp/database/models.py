from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    items = db.relationship('Item', backref='author', lazy='dynamic')

    def __init__(self, data):
        self.description = data.get('description', None)
        self.created_at = datetime.utcnow()
        for item in data.get('items'):
            self.items.append(Item(item))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    content_type = db.Column(db.String(100))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

    def __init__(self, data):
        self.created_at = datetime.utcnow()
        self.content_type = data.get('content_type')

    def __repr__(self):
        return "<Item {} >".format(self.id)


class Blob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    content_type = db.Column(db.String(100))
    content_hash = db.Column(db.String(100))
    content_length = db.Column(db.Integer)

    def __init__(self, created_at, content_type, content_length, content_hash):
        self.created_at = datetime.utcnow()
        self.content_type = content_type
        self.content_length = content_length
        self.content_hash = content_hash

    def __repr__(self):
        return "<Blob {} (Size: {}, Type: {}) >".format((self.id,
                    self.content_length, self.content_type))

