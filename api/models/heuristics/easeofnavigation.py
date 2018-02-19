from models.heuristic import Heuristic
from boilerpipe.extract import Extractor

# Formal 3
# Ensure ease of user navigation.
class EaseOfNavigation(Heuristic):
    def score(self, eula):

        if eula.html is not None:
            # gets actual text since eula.text doesn't get everything
            extractor = Extractor(extractor='KeepEverythingExtractor', html= eula.html)
            text = extractor.getText()
        else:
            text = eula.text

        # limit text to first 1000 characters
        text_first_1000 = text[:1000]
        tocscore = 0 # score for table of contents
        reason = '' # reason
        index_of_table = -1 # index of matching text

        # text to look out for
        tocindicators = ['TABLE OF CONTENTS', 'Table Of Contents']

        # find index of indicator text
        for ind in tocindicators:
            if index_of_table < 0:
                index_of_table = text_first_1000.find(ind)
            else:
                break

        # Score of 4 if found, score of 0 if not
        # TODO: additional scoring hyperlinked vs unlinked table
        tocscore = 4 if index_of_table >= 0 else 0

        return {'score': tocscore, 'max': 4, 'index': index_of_table}