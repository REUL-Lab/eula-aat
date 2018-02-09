from models.heuristic import Heuristic


# Ensure reasonable document length for target user
class DocumentLength(Heuristic):
    def score(self, input):
        return {'score': 5, 'max': 5}