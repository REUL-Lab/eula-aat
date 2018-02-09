from models.heuristic import Heuristic

# Ensure readability of EULA on mobile devices
class MobileReadability(Heuristic):
    def score(self, input):
        return {'score': 5, 'max': 5}