from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    def __init__(self, id, description=None, created_at = datetime.utcnow(),
            items=[]):
        pass
