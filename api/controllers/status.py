from flask import Flask
from flask_restful import reqparse, Resource

class Status(Resource):

    def get(self):
        return {'version' : '0.01'}