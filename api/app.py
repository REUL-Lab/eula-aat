#!/usr/bin/python
import os

from flask import Flask, Blueprint, g
from flask_restful import Resource, Api, url_for
from flask_pymongo import PyMongo
from common import auth

from controllers import input, status, results

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eula_aat'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
# app.config['MONGO_USERNAME'] = 'api'
# app.config['MONGODB_PASSWORD'] = os.environ['mongodb_pw']

api = Api(app)

api.add_resource(input.Upload, '/api/eula/upload')
api.add_resource(input.Fetch, '/api/eula/fetch')
api.add_resource(results.Results, '/api/results/<string:result_id>')
api.add_resource(status.Status, '/api/eula/status')

if __name__ == '__main__':
    app.run(debug=True)
