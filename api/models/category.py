""" Abstract class for Heuristics to extend.  All Heuristics should be able to be called using a single evaluate() call
"""

from abc import ABCMeta, abstractmethod

class Category:

    @abstractmethod
    def evaluate(input):
        """Primary method in the Heuristics class.  Returns a dict of scores for each part of the heuristic

        Args:
            input: The EULA object corresponding to an upload or query

        Returns:
            A dict of values for each score in a heuristic.
                The first entry should be a 'weighted' attribute between 0 and 5 with 2 degrees of precision.
                The other entries should be integers between 0 and 5, with 0 being an 'F' grade and 5 being an 'A' grade.

        Examples:
            >>> print(Substantive.score(my_eula))
            {'Weighted': 1.5, 'PlainLanguage': 5, 'DataCollection': 0, 'GagwrapClauses': 1}

        """
        pass