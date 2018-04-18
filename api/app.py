#!/usr/bin/python
import os

from flask import Flask, Blueprint, g
from flask_cors import CORS
from flask_restful import Resource, Api, url_for
from flask_pymongo import PyMongo

from controllers import input, status, results

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eula_aat'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017

app = Flask(__name__)
CORS(app)

api = Api(app)

api.add_resource(input.Upload, '/api/eula/upload')
api.add_resource(input.Fetch, '/api/eula/fetch')
api.add_resource(results.Results, '/api/results/<string:result_id>')
api.add_resource(status.Status, '/api/status')

if __name__ == '__main__':
    app.run(debug=True)
