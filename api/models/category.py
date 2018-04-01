""" Abstract class for Heuristics to extend.  All Heuristics should be able to be called using a single evaluate() call
"""

from abc import ABCMeta, abstractmethod
from multiprocessing import BoundedSemaphore, Process, Manager

class Category:

    @abstractmethod
    def evaluate(self, eula, thread_semaphore, ret_dict):
        """Primary method in the Heuristics class. Proxy for threaded method below

        Args:
            eula: The EULA object corresponding to an upload or query
            thread_semaphore: the semaphore to be released when we are done processing
            ret_dict: the thread-safe dictionary

        Examples:
            >>> Substantive.score(my_eula, semaphore, ret_dict)
            >>> print(ret_dict['substantive'])
            {'Weighted': 1.5, 'PlainLanguage': {...}, 'DataCollection': {...}, 'GagwrapClauses': {...}}

        """
        pass

    def parallel_evaluate(self, eula, heuristics, weights, thread_semaphore):
        """Thread support

        Args:
            eula: The EULA object corresponding to an upload or query

        Returns:
            A dict of values for each score in a heuristic.
                The first entry should be a 'weighted' attribute between 0 and 5 with 2 degrees of precision.
                The other entries should be integers between 0 and 5, with 0 being an 'F' grade and 5 being an 'A' grade.

        Examples:
            >>> print(Substantive.score(my_eula))
            {'Weighted': 1.5, 'PlainLanguage': 5, 'DataCollection': 0, 'GagwrapClauses': 1}

        """

        # Create our own manager for our subprocesses
        ret_vars = Manager().dict()

        # Create a process declaration for each category in the above array
        processes = []
        for heur in heuristics:
            # Describe the process, giving the eula
            processes.append(Process(target=heur().parallel_score, args=(eula, thread_semaphore, ret_vars)))

        # Start processes in order of above array
        for process in processes:
            # Aquire semaphore before starting
            thread_semaphore.acquire()
            # Start process once sempahore aquired
            process.start()

        # Join each process so we don't exit until all are done
        for process in processes:
            process.join()

        # Processing is done, so convert into regular dict
        ret_vars = ret_vars.copy()
        ret_vars_array = [v for k, v in ret_vars.items()]


        # Calculated weighted score for each return, but only if the score is valid.  Convert to float to maintain decimals until return
        weighted_scores = {k:float(v['score'])/v['max'] * weights[k] for k,v in ret_vars.iteritems() if v['score'] >= 0}
        # Sum the weights of the scores we are using to calculate overall
        sum_weights = sum({x:weights[x] for x in weights if x in weighted_scores}.values())
        # Return the overall weighted score which exists on a scale of [0-4]
        weighted_score = int((4 * sum(weighted_scores.values()) / sum_weights) if sum_weights > 0 else -1)

        return {
            'weighted_score': weighted_score,
            'heuristics': ret_vars_array
        }
