from models.heuristic import Heuristic

# Procedural 1a
# Ensure contrast of EULA link with background on mobile devices
class MobileAccessibility(Heuristic):
    @staticmethod
    def score(eula):
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}
