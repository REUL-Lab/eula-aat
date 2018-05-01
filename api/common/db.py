""" Manages database connections on a per-worker limit
"""

from flask import g, current_app
from pymongo import MongoClient

def get_db():
    # Only create a database instance if it's not already available
    db = getattr(g, '_database', None)
    app = current_app._get_current_object()

    if db is None:
        # Mongoclient is always localhost, but it is unprotected so a firewall must be set up.
        db = g._database = MongoClient('mongodb://localhost:27017/')['eula-aat']
    return db