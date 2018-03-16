from models.heuristic import Heuristic

# Formal 3
# Ensure ease of user navigation.
class EulaRetention(Heuristic):
    def score(self, eula):

        if not eula.html:
            return {'score': -1, 'max': 4, 'reason': 'Not Applicable'}

        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}