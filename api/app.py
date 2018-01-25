#!/usr/bin/python

from flask import Flask, Blueprint
from flask_restful import Resource, Api, url_for
from common import auth
from resources import heuristic, upload

app = Flask(__name__)
api = Api(app)

api.add_resource(upload.Upload, '/api/fetch')

if __name__ == '__main__':
    app.run(debug=True)