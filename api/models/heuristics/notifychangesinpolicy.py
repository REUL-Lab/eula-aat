from models.heuristic import Heuristic
import re

#procedural 7a

class NotifyChangesInPolicy(Heuristic):
    def score(self, eula):
        text = eula.text
        name = 'Notify Changes in Policy'
        description = ['Checks if this EULA gives notification to changes in policy']
        grade = 'NR'
        score = 4
        max = 4
        foundnotification = False

        #date format: any number formatting 26-1-2011 or 1/26/2011
        if re.search(r'(updated|modified|changed)\W*\s*(\d+\W\d+\W\d+)', text, re.IGNORECASE):
            foundnotification = True
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: January 26, 2011
        elif re.search(r'(updated|modified|changed)\W*\s*(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\s*\d+\W*\s*\d', text, re.IGNORECASE):
            foundnotification = True
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: Jan. 26, 2011
        elif re.search(r'(updated|modified|changed)\W*(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+\W*\d', text, re.IGNORECASE):
            foundnotification = True
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: 26 January 2011
        elif re.search(r'(updated|modified|changed)\W*(\d\W*)+(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\W*\d', text, re.IGNORECASE):
            foundnotification = True
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: 26 Jan. 2011
        elif re.search(r'(updated|modified|changed)\W*(\d\W*)+(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d',text, re.IGNORECASE):
            # return {'score': 4, 'max': 4, 'foundnotification': True}
            foundnotification = True

        # return {'score': 0, 'max': 4, 'foundnotification': False}
        else:
            score = 0
            foundnotification = False

        return {
        'name'              : name,
        'description'       : description,
        'grade'             : grade,
        'score'             : score,
        'max'               : max,
        'foundnotification' : foundnotification
        }


