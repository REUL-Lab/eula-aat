""" Abstract class for Heuristics to extend.  All Heuristics should be able to be called using a single evaluate() call
"""
import traceback
import logging
from abc import ABCMeta, abstractmethod

class Heuristic:

    @abstractmethod
    def score(self, eula):
        """Primary method in the Heuristics class.  Returns a dict of scores for each part of the heuristic

        Args:
            eula: The EULA object corresponding to an upload or query

        """
        pass

    def parallel_score(self, eula, thread_semaphore, ret_vars):
        """Proxy method for score(self, eula) that handles threaded return and semaphore access

        Args:            
            eula: The EULA object corresponding to an upload or query
            thread_semaphore: The semaphore object to release once process is done
            ret_vars: the dictionary to place our return values in

        """
        try:
            # Run in a try-catch to prevent runaway threads
            ret_vars[self.__class__.__name__.lower()] = self.score(eula)
        except Exception as e:
            # Log the error since we've caught it
            logging.error(traceback.format_exc())
        finally:
            # Always make sure semaphore is released
            thread_semaphore.release()
