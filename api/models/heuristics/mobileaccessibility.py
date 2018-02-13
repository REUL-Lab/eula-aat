from models.heuristic import Heuristic

# Ensure contrast of EULA link with background on mobile devices
class MobileAccessibility(Heuristic):
    def score(self, eula):
        if eula.mobile_render is None:
            return {'score': -1, 'max': 5, 'reason': 'no render'}
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}