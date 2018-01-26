""" Contains the Substantive heuristic sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic

def evaluate(input):
    return {'Weighted': 2.5, 'PlainLanguage': PlainLanguage().score(input)} #TODO


class PlainLanguage(Heuristic):

    def score(self, input):
        return 5