""" Abstract class for categories to extend.  All categories should use the @abstractmethod tag when implementing this
"""

from abc import ABCMeta, abstractmethod
from multiprocessing import BoundedSemaphore, Process, Manager

class Category:

    @abstractmethod
    def get_heuristics():
        """Getter for the heuristics in a category
        
        Returns:
            A dict of values for each score in a heuristic.
                Keys should be the class definitions for a heuristic, and values should be the weight

        Examples:
            >>> print(Substantive.get_heuristics)
            {PlainLanguage: 5, DataCollection: 0, GagwrapClause: 1}
        
        """
        pass