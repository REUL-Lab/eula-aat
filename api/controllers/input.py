import os
import requests
import time
from flask import Flask, g
from flask_restful import reqparse, Resource
from werkzeug.datastructures import FileStorage

from common import auth, db, webfetch
from models import eula, formal, substantive, procedural

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
        cleanup_tasks = {}

        try:
            text = fetcher.extract_text()
            html = fetcher.get_html()
            desk_driver = fetcher.get_desk_driver()
            url = desk_driver.current_url
            mobile_driver = fetcher.get_mobile_driver()

            # Add cleanup tasks for both instances
            cleanup_tasks[desk_driver] = desk_driver.quit
            cleanup_tasks[mobile_driver] = mobile_driver.quit
            fetched_eula = eula.EULA(text, url=url, html=html, desk_driver=desk_driver, mobile_driver=mobile_driver)

            res = fetched_eula.analyze()

        finally:
            # Since we need the driver for a few heuristics, always make sure we close it or we will run out of memory
            #   giving it all to chrome
            for item, cleanup in cleanup_tasks.iteritems():
                cleanup()


        # Store results in mongodb and return the identifier for lookup
        return str(db.get_db().results.insert_one(res).inserted_id)


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

        res = uploaded_eula.analyze()

        # Store results in mongodb and return the identifier for lookup
        return str(db.get_db().results.insert_one(res).inserted_id)