#!/usr/bin/python
import os
from flask import Flask, Blueprint
from flask_restful import Resource, Api, url_for
from common import auth

from controllers import input, status

app = Flask(__name__)
api = Api(app)

api.add_resource(input.Upload, '/api/eula/upload')
api.add_resource(input.Fetch, '/api/eula/fetch')
api.add_resource(status.Status, '/api/eula/status')

if __name__ == '__main__':
    app.run(debug=True)
