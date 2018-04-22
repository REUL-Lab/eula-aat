import os, logging, traceback
from multiprocessing import BoundedSemaphore, Process, Manager

from models import category
from models.categories import substantive, procedural, formal

def analyze_eula(eula):
    # Categories to analyse, these will be done in parallel
    categories = [formal.Formal, procedural.Procedural, substantive.Substantive]

    # Create a semaphore to limit number of running processes
    running = BoundedSemaphore(int(os.getenv('analyze_max_threads', 1)))

    # We cannot return variables from threads, so instead create managed dictionary to pass objects back through
    ret_vars = Manager().dict()

    # Create a process declaration for each category in the above array
    processes = []
    for cat in categories:
        # Allocate a space in the dictionary for their return values
        ret_vars[cat.__name__.lower()] = None
        # Describe the process, giving the eula (us), the semaphore, and the return dict
        processes.append(Process(target=cat_score, args=(eula, cat, ret_vars, running)))

    # Start processes in order of above array
    for process in processes:
        # Start process once sempahore aquired
        process.start()

    # Join each process so we don't exit until all are done
    for process in processes:
        process.join()

    # De-parallelize dict now that we are done
    ret_vars = ret_vars.copy()

    # Calculate overall score by summing the weighted score of each category then dividing by number of categories
    # i.e. simple average
    overall_score = int(sum(map(lambda x: x['weighted_score'], ret_vars.values())) / len(ret_vars))
    grades = ['F', 'D', 'C', 'B', 'A']

    return {'title': eula.url, 'overall_score': overall_score, 'overall_grade': grades[overall_score], 'categories': ret_vars}

def cat_score(eula, cat, ret_var, thread_semaphore):
    """Category scoring with thread support

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

    # Extract the heuristics from the class
    heuristics = cat.get_heuristics()

    # Create a process declaration for each category in the above array
    processes = []
    for heur in heuristics.keys():
        # Describe the process, giving the eula
        processes.append(Process(target=heur_score, args=(heur, eula, thread_semaphore, ret_vars)))

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

    # Calculated weighted score for each return, but only if the score is valid.  Convert to float to maintain decimals until return
    weighted_scores = {k:float(v['score'])/v['max'] * heuristics[k] for k,v in ret_vars.iteritems() if v['score'] >= 0}
    # Sum the weights of the scores we are using to calculate overall
    sum_weights = sum({x:heuristics[x] for x in heuristics.keys() if x in weighted_scores}.values())
    # Return the overall weighted score which exists on a scale of [0-4]
    weighted_score = int((4 * sum(weighted_scores.values()) / sum_weights) if sum_weights > 0 else -1)

    # Map the class definitions to their names for returning
    ret_var[cat.__name__.lower()] = {
        'weighted_score': weighted_score,
        'heuristics': ret_vars.values()
    }

def heur_score(heur, eula, thread_semaphore, ret_vars):
    """Proxy method for score(self, eula) that handles threaded return and semaphore access

    Args:
        eula: The EULA object corresponding to an upload or query
        thread_semaphore: The semaphore object to release once process is done
        ret_vars: the dictionary to place our return values in

    """
    try:
        # Run in a try-catch to prevent runaway threads
        ret_vars[heur] = heur.score(eula)
    except Exception as e:
        # Log the error since we've caught it
        logging.error(traceback.format_exc())
    finally:
        # Always make sure semaphore is released
        thread_semaphore.release()
