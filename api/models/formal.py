""" Contains the Formal category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic

from heuristics import *

class Formal(Category):

    def evaluate(self, eula, running, ret_vars):
        heuristics_to_eval = [typeconventions.TypeConventions, easeofnavigation.EaseOfNavigation, documentlength.DocumentLength]
        heuristic_weights = {'typeconventions': 1, 'easeofnavigation': 1, 'documentlength': 1}

        # Parallel evaluate heuristics and add them to the dict when done
        ret_vars['formal'] = self.parallel_evaluate(eula, heuristics_to_eval, heuristic_weights, running)