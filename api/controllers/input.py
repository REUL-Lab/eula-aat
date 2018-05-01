""" Main feature of the backend.  Resources are either given as a URL or a txt file.  Results are stored in mongo and the mongo_id is handed back.
"""

import os
import requests
import time
from flask import Flask, g
from flask_restful import reqparse, Resource
from werkzeug.datastructures import FileStorage

from common import db, webfetch, analysis
from models import eula

class Fetch(Resource):
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

            fetched_eula = eula.EULA(text, title=desk_driver.title, url=url, html=html, desk_driver=desk_driver, mobile_driver=mobile_driver)

            res = analysis.analyze_eula(fetched_eula)

        finally:
            # Since we need the driver for a few heuristics, always make sure we close it or we will run out of memory
            #   giving it all to chrome
            for item, cleanup in cleanup_tasks.iteritems():
                cleanup()

        # Store results in mongodb and return the identifier for lookup
        return str(db.get_db().results.insert_one(res).inserted_id)


class Upload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('doctype', type=str, required=True)
        parser.add_argument('contents', type=FileStorage, required=True, location='files')

        vals = parser.parse_args()

        #
        if vals['doctype'] == 'txt':
            # Parse into ASCII for the readability calculator
            content = vals['contents'].read()
            # Ordinals between 0 and 128 are ASCII
            text = ''.join([i if ord(i) < 128 else '' for i in content])
            # Create eula object
            uploaded_eula = eula.EULA(text=text, title=vals['contents'].filename)
        else:
            abort(400, message='doctype string not recognized value')

        res = analysis.analyze_eula(uploaded_eula)

        # Store results in mongodb and return the identifier for lookup
        return str(db.get_db().results.insert_one(res).inserted_id)