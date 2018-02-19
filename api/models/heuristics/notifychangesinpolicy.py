# from models.heuristic import Heuristic
import re

class NotifyChangesInPolicy():
    def score(self, eula):
        text = eula.text

        if re.search(r'(updated|modified|changed)\W*\s*(\d+\W\d+\W\d+)', text, re.IGNORECASE):
            return {'score': 4, 'max': 4, 'found notification': True}

        elif re.search(r'(updated|modified|changed)\W*\s*(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\s*\d+\W*\s*\d', text, re.IGNORECASE):
            return {'score': 4, 'max': 4, 'found notification': True}

        elif re.search(r'(updated|modified|changed)\W*(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d+\W*\d', text, re.IGNORECASE):
            return {'score': 4, 'max': 4, 'found notification': True}

        elif re.search(r'(updated|modified|changed)\W*(\d\W*)+(January|February|March|April|May|June|July'
                       r'|August|September|October|November|December)+\W*\d', text, re.IGNORECASE):
            return {'score': 4, 'max': 4, 'found notification': True}

        elif re.search(r'(updated|modified|changed)\W*(\d\W*)+(Jan|Feb|Mar|Apr|May|Jun|Jul'
                       r'|Aug|Sep|Oct|Nov|Dec)+\W*\d',text, re.IGNORECASE):
            return {'score': 4, 'max': 4, 'found notification': True}

        return {'score': 0, 'max': 4, 'found notification': False}

