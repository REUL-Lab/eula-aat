from flask import abort
from flask_restful import Resource
from pymongo import collection
from bson.errors import InvalidId
from bson.objectid import ObjectId

from common import db

class Results(Resource):

    def get(self, result_id):
        try:
            res = db.get_db().results.find_one({'_id': ObjectId(result_id)})
            if res is not None:
                del res['_id']
                return res
            else:
                abort(404)
        except InvalidId:
            abort(400)