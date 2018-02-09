from flask import Flask
from flask_restful import reqparse, Resource
from common import auth
from models import eula, formal, substantive, procedural
from werkzeug.datastructures import FileStorage

class Fetch(Resource):
    # method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True)

        vals = parser.parse_args()

        uploaded_eula = eula.EULA(vals['url'])

        overall_score = 0
        categories = [formal.Formal, procedural.Procedural, substantive.Substantive]

        return {
            'overall_score': overall_score,
            'categories': dict((cat.__name__, cat().evaluate(uploaded_eula)) for cat in categories)
        }


class Upload(Resource):
    # method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('doctype', type=str, required=True)
        parser.add_argument('contents', type=FileStorage, required=True, location='files')

        vals = parser.parse_args()

        if vals['doctype'] == 'txt':
            uploaded_eula = eula.EULA(vals['contents'], vals['contents'].read())
        else:
            abort(400, message='doctype string not recognized value')

        overall_score = 0
        categories = [formal.Formal, procedural.Procedural, substantive.Substantive]

        return {
            'overall_score': overall_score,
            'categories': dict((cat.__name__, cat().evaluate(uploaded_eula)) for cat in categories)
        }