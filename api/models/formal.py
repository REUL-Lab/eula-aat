""" Contains the Formal category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic

from heuristics import *

class Formal(Category):

    def evaluate(self, input):
        heuristics_to_eval = [typeconventions.TypeConventions, easeofnavigation.EaseOfNavigation, documentlength.DocumentLength]
        
        weighted_score = 0
        heuristic_scores = dict((heur.__name__.lower(), heur().score(input)) for heur in heuristics_to_eval)

        return {
            'weighted_score': weighted_score,
            'heuristics': heuristic_scores
        }
