from flask import abort
from flask_restful import Resource
from pymongo import collection
from bson.errors import InvalidId
from bson.objectid import ObjectId

from common import db

class Results(Resource):

    def get(self, result_id):
        try:
            # Find result by id propert
            res = db.get_db().results.find_one({'_id': ObjectId(result_id)})
            if res is not None:
                # delete the mongodb portion for the raw result and return
                del res['_id']
                return res
            else:
                # not found in db, so throw 404
                abort(404)
        except InvalidId:
            # IDs can be invalid, so throw a 400 if it's not recognizable by mongo
            abort(400)