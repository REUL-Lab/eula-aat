from models.heuristic import Heuristic

# Procedural 1b
# Ensure readability of EULA on mobile devices
class MobileReadability(Heuristic):
    def score(self, eula):
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}
