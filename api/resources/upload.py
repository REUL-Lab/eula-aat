from flask import Flask
from flask_restful import reqparse, Resource
from common import auth

class Upload(Resource):
    method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True)

        vals = parser.parse_args()

        return {'grade': 'best eula ever', 'url': vals['url']}
