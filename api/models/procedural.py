""" Contains the Procedural category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic
from heuristics import *

class Procedural(Category):

    def evaluate(self, eula, thread_semaphore, ret_vars):
        # List of heuristics to evaluate, and the relative weighting of each
        heuristics_to_eval = [mobileaccessibility.MobileAccessibility, mobilereadability.MobileReadability]
        heuristic_weights = {'mobileaccessibility': 2, 'mobilereadability': 5}

        ret_vars['procedural'] = self.parallel_evaluate(eula, heuristics_to_eval, heuristic_weights, thread_semaphore)
