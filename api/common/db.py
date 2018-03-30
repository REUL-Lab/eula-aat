from flask import g, current_app
from pymongo import MongoClient

def get_db():
    db = getattr(g, '_database', None)
    app = current_app._get_current_object()

    if db is None:
        db = g._database = MongoClient('mongodb://localhost:27017/')['eula-aat']
    return db