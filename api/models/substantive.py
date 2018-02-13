""" Contains the Substantive category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic

from heuristics import *

class Substantive(Category):

    
    def evaluate(self, eula):
        heuristics_to_eval = [plainlanguage.PlainLanguage]
        heuristic_weights = {'plainlanguage': 1}

        # Iteratively evaluate each heuristic in the above list
        heuristic_scores = dict((heur.__name__.lower(), heur().score(eula)) for heur in heuristics_to_eval)

        # Calculated weighted score for each return, but only if the score is valid.  Convert to float to maintain decimals until return
        weighted_scores = {k:float(v['score'])/v['max'] * heuristic_weights[k] for k,v in heuristic_scores.iteritems() if v['score'] >= 0}
        # Sum the weights of the scores we are using to calculate overall
        sum_weights = sum({x:heuristic_weights[x] for x in heuristic_weights if x in weighted_scores}.values())
        # Return the overall weighted score which exists on a scale of [0-4]
        weighted_score = int((4 * sum(weighted_scores.values()) / sum_weights) if sum_weights > 0 else -1)

        return {
            'weighted_score': weighted_score,
            'heuristics': heuristic_scores
        }