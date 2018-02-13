import os
import requests

from flask import Flask
from flask_restful import reqparse, Resource
from common import auth, webfetch
from models import eula, formal, substantive, procedural
from werkzeug.datastructures import FileStorage

class Fetch(Resource):
    # method_decorators = [auth.authenticate]

    def post(self):
        # Parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True)
        vals = parser.parse_args()

        try:
            fetcher = webfetch.FetchService(vals['url'])
        except requests.ConnectionError as e:
            return {'error': 'Could not fetch from URL - Error {0}'.format(e)}

        # Make sure driver variable is declared because we *CAN NOT* leave the driver open
        driver = None

        try:
            text = fetcher.extract_text()
            desktop = fetcher.desktop_render()
            mobile = fetcher.mobile_render()
            html = fetcher.get_html()
            driver = fetcher.get_driver()

            uploaded_eula = eula.EULA(text, html=html, driver=driver, desktop_render=desktop, mobile_render=mobile)

            categories = [formal.Formal, procedural.Procedural, substantive.Substantive]
            cat_scores = dict((cat.__name__.lower(), cat().evaluate(uploaded_eula)) for cat in categories)

            # Calculate overall score by summing the weighted score of each category then dividing by number of categories
            # i.e. simple average
            overall_score = int(sum(map(lambda x: x['weighted_score'], cat_scores.values())) / len(cat_scores))
        finally:
            # Since we need the driver for a few heuristics, always make sure we close it or we will run out of memory
            #   giving it all to chrome
            if driver is not None:
                driver.quit()

        return {
            'overall_score': overall_score,
            'categories': cat_scores
        }


class Upload(Resource):
    # method_decorators = [auth.authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('doctype', type=str, required=True)
        parser.add_argument('contents', type=FileStorage, required=True, location='files')

        vals = parser.parse_args()

        if vals['doctype'] == 'txt':
            uploaded_eula = eula.EULA(vals['contents'].read())
        else:
            abort(400, message='doctype string not recognized value')

        # Select categories for evaluation and process each iteratively
        categories = [formal.Formal, procedural.Procedural, substantive.Substantive]
        cat_scores = dict((cat.__name__.lower(), cat().evaluate(uploaded_eula)) for cat in categories)

        # Calculate overall score by summing the weighted score of each category then dividing by number of categories
        # i.e. simple average
        overall_score = int(sum(map(lambda x: x['weighted_score'], cat_scores.values())) / len(cat_scores))

        return {
            'overall_score': overall_score,
            'categories': cat_scores
        }