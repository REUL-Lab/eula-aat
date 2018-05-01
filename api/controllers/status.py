""" Simple status page to test if the API is responding to requests.
"""

from flask import Flask
from flask_restful import reqparse, Resource

class Status(Resource):

    def get(self):
        return {'version' : '1.0'}