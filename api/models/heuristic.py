""" Abstract class for Heuristics to extend.  All Heuristics should be able to be called using a single evaluate() call
"""

from abc import ABCMeta, abstractmethod

class Heuristic:

    @abstractmethod
    def score(input):
        """Primary method in the Heuristics class.  Returns a dict of scores for each part of the heuristic

        Args:
            input: The EULA object corresponding to an upload or query

        Returns:
            A single integer value between 0 and 5.

        Examples:
            >>> print(PlainLanguage.score(my_eula))
            5

        """
        pass