from models.heuristic import Heuristic
import re

class NotifyChangesInPolicy(Heuristic):
    def score(self, eula):
        text = eula.text
        wordlist = ["last modified", "last updated", "last changed"]
        for word in wordlist:
            if (word in text.lower()):
                return {'score': 4, 'max': 4, 'found notification': True}

        match = re.search(r'(updated|modified|changed)\W\s*(\d+/\d+/\d+)', text, re.IGNORECASE)

        if (match != None):
            return {'score': 4, 'max': 4, 'found notification': True}

        match = re.search(r'(updated|modified|changed)\W\s*((January|February|March|April|May|June|July'
                          r'|August|September|October|November|December)+\s*\d+\W\s*\d)',
                          text, re.IGNORECASE)

        if (match != None):
            return {'score': 4, 'max': 4, 'found notification': True}

        return {'score': 0, 'max': 4, 'found notification': False}