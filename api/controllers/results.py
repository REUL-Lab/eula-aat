from flask import Flask, g
from flask_restful import reqparse, Resource
from pymongo import collection
from bson.objectid import ObjectId

from common import db

class Results(Resource):

    def get(self, result_id):
        res = db.get_db().results.find_one({'_id': ObjectId(result_id)})
        del res['_id']
        return res

