from models.heuristic import Heuristic
from flask import Flask
import urllib
import urllib2
import os
import json

# Keys are specified in https://developers.google.com/webmaster-tools/search-console-api/reference/rest/v1/urlTestingTools.mobileFriendlyTest/run#MobileFriendlyIssue
grade_ratios = {
    'MOBILE_FRIENDLY_RULE_UNSPECIFIED': 0,
    'USES_INCOMPATIBLE_PLUGINS': 0,
    'CONFIGURE_VIEWPORT': 3,
    'FIXED_WIDTH_VIEWPORT': 5,
    'SIZE_CONTENT_TO_VIEWPORT': 5,
    'USE_LEGIBLE_FONT_SIZES': 10,
    'TAP_TARGETS_TOO_CLOSE': 2
}

humanized_issues = {
    'USES_INCOMPATIBLE_PLUGINS': 'Some of the plugins used by your site do not support mobile browsers',
    'CONFIGURE_VIEWPORT': 'The viewport of your page is not configured to adapt to mobile browsers',
    'FIXED_WIDTH_VIEWPORT': 'The viewport of your page is fixed-width',
    'SIZE_CONTENT_TO_VIEWPORT': 'The size of the static content (e.g. images) in your viewport is incorrect',
    'USE_LEGIBLE_FONT_SIZES': 'The font size for your page is too small for mobile browsers',
    'TAP_TARGETS_TOO_CLOSE': 'Targets or links in your page are too close for mobile "tapping"',
    'NO_ISSUES': 'No mobile readability issues were found in this EULA!'
}

grades = ['F', 'D', 'C', 'B', 'A']

# Procedural 1b
# Ensure readability of EULA on mobile devices
class MobileReadability(Heuristic):

    @staticmethod
    def score(eula):
        # Create string keyed dictionary for conversion into JSON at end
        ret_vals = {
            'name': 'Mobile Readability',
            'description': 'Assesses the readability of a EULA on a web-page',
            'feedback': [],
            'max': 4
        }

        if eula.url is None:
            ret_vals['feedback'] = ['This EULA was an uploaded document and therefore does not have a mobile view.']
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            return ret_vals

        # Fetch API key from env var
        # If key does not load, omit this heuristic
        if 'google_api_key' not in os.environ:
            raise 'google_api_key not found in environment variables'
            
        google_api_key = os.environ['google_api_key']
        service_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key={0}".format(google_api_key)

        # Parameters to send to google URL
        params = {
            'url': eula.url
        }

        # Open connection and read data back
        content = json.loads(urllib2.urlopen(url=service_url, data=urllib.urlencode(params)).read())

        # Make sure test ran properly
        if content['testStatus']['status'] != 'COMPLETE':
            ret_vals['reason'] = 'Could not connect to Google APIs (NOKEY)'
            ret_vals['score'] = -1
            ret_vals['grade'] = 'N/R'
            return ret_vals

        # If there are no issues or no reason to deduct (might be redundent, but is safer way to reference api), return our score
        if content['mobileFriendliness'] == "MOBILE_FRIENDLY" or 'mobileFriendlyIssues' not in content:
            ret_vals['reason'] = 'Could not connect to Google APIs (NOKEY)'
            ret_vals['score'] = 4
            ret_vals['grade'] = grades[4]
            return ret_vals

        # If there are issues
        if 'mobileFriendlyIssues' in content:
            # Extract issues into a single array
            issues = map(lambda x: x['rule'], content['mobileFriendlyIssues'])
            # Start by considering the entire denominator
            denom = sum(grade_ratios.values())
            num = float(denom)

            # Subtract from numerator for each issue, relative to the weights at top
            for issue in issues:
                num = num - grade_ratios[str(issue)]
                ret_vals['feedback'].append(humanized_issues[str(issue)])

            if len(ret_vals['feedback']) == 0:
                ret_vals['feedback'].append(humanized_issues['NO_ISSUES'])

            # Multiply score by 4 for our even representation
            ret_vals['score'] = int(round(4 * num / denom))
            # Assign grade to score
            ret_vals['grade'] = grades[ret_vals['score']]

            # Make final return call
            return ret_vals
            