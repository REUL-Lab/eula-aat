from models.heuristic import Heuristic

# Formal 3
# Ensure ease of user navigation.
class EaseOfNavigation(Heuristic):
    def score(self, eula):
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}