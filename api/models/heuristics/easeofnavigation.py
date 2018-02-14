from models.heuristic import Heuristic
from boilerpipe.extract import Extractor

# Formal 3
# Ensure ease of user navigation.
class EaseOfNavigation(Heuristic):
    def score(self, eula):
        extractor = Extractor(extractor='KeepEverythingExtractor', html= eula.html)
        text = extractor.getText()
        text1000 = text[:1000]
        tocscore = 0
        reason = ''
        indexOfTable = -1

        tocindicators = ['TABLE OF CONTENTS', 'Table Of Contents']

        for ind in tocindicators:
            if indexOfTable < 0:
                indexOfTable = text1000.find('TABLE OF CONTENTS')
            else:
                break
        
        if indexOfTable < 0:
            tocscore = 0
            reason += 'No table of contents found near beginning of EULA. '
        else:
            tocscore = 4
            reason += 'Found table of contents. '


        return {'score': tocscore, 'max': 4, 'reason': reason, 'text': text1000}