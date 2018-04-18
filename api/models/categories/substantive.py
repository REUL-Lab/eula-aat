""" Contains the Substantive category sum and the sub heuristics
"""

from models.category import Category
from models.heuristics import plainlanguage

class Substantive(Category):

    @staticmethod
    def get_heuristics():
        return {
            plainlanguage.PlainLanguage: 1
        }