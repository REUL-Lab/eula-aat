from models.heuristic import Heuristic
import re

#procedural 7a

class NotifyChangesInPolicy(Heuristic):

    @staticmethod
    def score(eula):
        text = eula.text
        name = 'Notify Changes in Policy'
        description = ['Checks if this EULA gives notification to changes in policy']
        feedback = []
        grade = 'NR'
        score = 4
        max = 4
        foundnotification = False
        date = None

        #date format: any number formatting 26-1-2011 or 1/26/2011
        if re.search(r'(updated|modified|changed)\W*\s*(\d+\W\d+\W\d+)', text, re.IGNORECASE):
            date = re.search(r'(updated|modified|changed)\W*\s*(\d+\W\d+\W\d+)', text, re.IGNORECASE)
            foundnotification = True
            grade = 'A'
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: January 26, 2011
        elif re.search(r'(updated|modified|changed)\W*\s*(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\s*\d+\W*\s*\d+', text, re.IGNORECASE):
            date = re.search(r'(updated|modified|changed)\W*\s*(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\s*\d+\W*\s*\d+', text, re.IGNORECASE)
            foundnotification = True
            grade = 'A'
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: Jan. 26, 2011
        elif re.search(r'(updated|modified|changed)\W*(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+\W*\d+', text, re.IGNORECASE):
            date = re.search(r'(updated|modified|changed)\W*(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+\W*\d+', text, re.IGNORECASE)
            foundnotification = True
            grade = 'A'
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: 26 January 2011
        elif re.search(r'(updated|modified|changed)\W*(\d+\W*)+(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\W*\d+', text, re.IGNORECASE):
            date = re.search(r'(updated|modified|changed)\W*(\d+\W*)+(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\W*\d+', text, re.IGNORECASE)
            foundnotification = True
            grade = 'A'
            # return {'score': 4, 'max': 4, 'foundnotification': True}
        #date format: 26 Jan. 2011
        elif re.search(r'(updated|modified|changed)\W*(\d+\W*)+(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+',text, re.IGNORECASE):
            date = re.search(r'(updated|modified|changed)\W*(\d+\W*)+(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+',text, re.IGNORECASE)
            # return {'score': 4, 'max': 4, 'foundnotification': True}
            foundnotification = True
            grade = 'A'

        # return {'score': 0, 'max': 4, 'foundnotification': False}
        else:
            score = 0
            grade = 'F'
            foundnotification = False

        if date is not None:
            feedback.append("Your EULA states \"{0}\"".format(date.group(0)))
        else:
            feedback.append("The tool did not find a last-modified date in your EULA")

        retvars = {
            'name': name,
            'description': description,
            'grade': grade,
            'score': score,
            'max': max,
            'foundnotification' : foundnotification,
            'feedback': feedback
        }

        if date is not None:
            retvars['date'] = date.group(0)

        return retvars
