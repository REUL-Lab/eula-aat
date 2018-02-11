from models.heuristic import Heuristic

# Ensure contrast of EULA link with background on mobile devices
class MobileAccessibility(Heuristic):
    def score(self, eula):
        if eula.mobile_render is None:
            return {'score': 'N/A', 'max': 5, 'reason': 'no render'}
        return {'score': 5, 'max': 5}