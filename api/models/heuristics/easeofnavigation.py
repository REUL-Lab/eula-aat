from models.heuristic import Heuristic


class EaseOfNavigation(Heuristic):
    def score(self, eula):
        return {'score': -1, 'max': 4, 'reason': 'Not implemented'}