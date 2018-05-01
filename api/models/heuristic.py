""" Abstract class for Heuristics to extend.  All Heuristics should be able to be called using a single score() call
"""
import traceback
import logging
from abc import ABCMeta, abstractmethod

class Heuristic:

    @abstractmethod
    def score(eula):
        """Primary method in the Heuristics class.  Returns a dict of scores for each part of the heuristic

        Args:
            eula: The EULA object corresponding to an upload or query

        """
        pass