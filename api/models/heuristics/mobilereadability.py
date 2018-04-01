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

# Procedural 1b
# Ensure readability of EULA on mobile devices
class MobileReadability(Heuristic):
    def score(self, eula):
        name = 'Mobile Readability'
        grade = 'NR'
        description = ['default description']
        score = -1
        max = 4
        reason = 'default'
        issues = None

        def ret_vals():
            return {
            'name' : name,
            'grade' : grade,
            'description' : description,
            'score' : score,
            'max' : max,
            'reason' : reason,
            'issues' : issues
            }


        if eula.url is None:
            # return {'score': -1, 'max': 4, 'reason': 'no url'}
            reason = 'no url'
            return ret_vals()

        # Fetch API key from env var
        # If key does not load, omit this heuristic
        if 'google_api_key' not in os.environ:
            # return {'score': -1, 'max': 4, 'reason': 'Could not connect to Google APIs (NOKEY)'}
            reason = 'Could not connect to Google APIs (NOKEY)'
            return ret_vals()

        try:
            google_api_key = os.environ['google_api_key']
            service_url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'

            # Parameters to send to google URL
            params = {
                'url': eula.url,
                'key': google_api_key
            }

            # Open connection and read data back
            content = json.loads(urllib2.urlopen(url=service_url, data=urllib.urlencode(params)).read())

            # Make sure test ran properly
            if content['testStatus']['status'] != 'COMPLETE':
                # return {'score': -1, 'max': 4, 'reason': 'Could not connect to Google APIs'}
                reason = 'Could not connect to Google APIs'
                return ret_vals()

            # If there are no issues or no reason to deduct (might be redundent, but is safer way to reference api), return our score
            if content['mobileFriendliness'] == "MOBILE_FRIENDLY" or 'mobileFriendlyIssues' not in content:
                return {'score': 4, 'max': 4}

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

                # # Create string keyed dictionary for conversion into JSON at end
                # retscore = {
                #     # Multiply score by 4 for our even representation
                #     'score': int(round(4 * num / denom)),
                #     'max': 4
                # }
                score = int(round(4 * num / denom))
                # Add issues to the return score if we have them
                # if len(issues) > 0:
                #     retscore['issues'] = issues

                # Make final return call
                return ret_vals()


        except urllib2.URLError:
            reason = 'Could not connect to Google APIs'
            return ret_vals()
        except KeyError:
            reason = 'Error parsing Google API Result'
            return ret_vals()
