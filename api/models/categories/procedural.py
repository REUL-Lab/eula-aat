""" Contains the Procedural category sum and the sub heuristics
"""

from models.category import Category
from models.heuristics import mobileaccessibility, notifychangesinpolicy, mobilereadability

class Procedural(Category):

    @staticmethod
    def get_heuristics():
        return {
            mobileaccessibility.MobileAccessibility: 2,
            notifychangesinpolicy.NotifyChangesInPolicy: 3,
            mobilereadability.MobileReadability: 5
        }