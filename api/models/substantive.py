""" Contains the Substantive category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic
from heuristics import *

class Substantive(Category):

    def evaluate(self, eula, thread_semaphore, ret_vars):
        heuristics_to_eval = [plainlanguage.PlainLanguage]
        heuristic_weights = {'plainlanguage': 1}

        # Parallel evaluate heuristics and add them to the dict when done
        ret_vars['substantive'] = self.parallel_evaluate(eula, heuristics_to_eval, heuristic_weights, thread_semaphore)
