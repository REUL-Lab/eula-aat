from models.heuristic import Heuristic

# Procedural 1a
# Ensure contrast of EULA link with background on mobile devices
class MobileAccessibility(Heuristic):
    def score(self, eula):
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}
