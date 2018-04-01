from models.heuristic import Heuristic

# Formal 3
# Ensure ease of user navigation.
class EaseOfNavigation(Heuristic):
    def score(self, eula):
        name = 'Ease Of Navigation'
        grade = 'NR'
        description = ['this heuristic is not yet implemented']
        return {
        'name'        : name,
        'grade'       : grade,
        'description' : description,
        'score'       : -1,
        'max'         : 4,
        'reason'      : 'Not implemented'
        }
