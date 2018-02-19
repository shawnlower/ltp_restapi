"""
Database setup routines
"""

from .models import db

def setup_db(drop_db=False):
    if drop_db:
        db.drop_all()
    db.create_all()
