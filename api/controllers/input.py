from flask import Flask
from flask_restful import reqparse, Resource
from common import auth
from models import eula, substantive

class Fetch(Resource):
    method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True)

        vals = parser.parse_args()

        uploaded_eula = eula.EULA(vals['url'])


        return {'substantive': substantive.evaluate(uploaded_eula), 'url': vals['url']}


class Upload(Resource):
    method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()

        vals = parser.parse_args()

        return {'grade': 'best eula ever'}