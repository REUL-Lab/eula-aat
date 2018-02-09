""" Contains the Formal category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic


from heuristics.typeconventions import TypeConventions
from heuristics.easeofnavigation import EaseOfNavigation
from heuristics.documentlength import DocumentLength

class Formal(Category):

    def evaluate(self, input):
        heuristics_to_eval = [TypeConventions, EaseOfNavigation, DocumentLength]
        
        weighted_score = 0
        heuristic_scores = dict((heur.__name__, heur().score(input)) for heur in heuristics_to_eval)

        return {
            'weighted_score': weighted_score,
            'heuristics': heuristic_scores
        }
