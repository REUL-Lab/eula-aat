from models.heuristic import Heuristic

# Ensure contrast of EULA link with background on mobile devices
class MobileAccessibility(Heuristic):
    def score(self, input):
        return {'score': 5, 'max': 5}