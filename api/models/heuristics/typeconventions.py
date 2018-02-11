from models.heuristic import Heuristic

class TypeConventions(Heuristic):
    def score(self, eula):
        return {'score': 5, 'max': 5}