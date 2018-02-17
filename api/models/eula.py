""" This file should contain only a single class, EULA.  It is to be the object representation of a user-provided EULA
"""
import os
from multiprocessing import BoundedSemaphore, Process, Manager

import category, substantive, procedural, formal

class EULA:

    """Class for EULAs.  Both input methods should create a EULA object with the full set of instance variables.

    A EULA

    Note:
        The page of a EULA should be done inside of this class.  The input sources should only provide the URL/File.

    Args:
        URL: the accessible URL for a EULA.  If the user uploads a PDF, this should be the temp stored html-ized version of that PDF

    Attributes:
        text: the parsed text of the EULA, containing no formatting and ASCII format text only
        url: the URL of the EULA (if applicable)
        html: the html of the desktop session
        desk_driver: the selenium driver for the headless desktop instance
        mobile_driver: the selenium driver for the headless mobile instance

    """

    def __init__(self, text, url=None, html=None, desk_driver=None, mobile_driver=None):
        self.text = text
        self.url = url
        self.html = html
        self.desk_driver = desk_driver
        self.mobile_driver = mobile_driver


    def analyze(self):
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
            processes.append(Process(target=cat().evaluate, args=(self, running, ret_vars)))

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

        return {'overall_score': overall_score, 'categories': ret_vars}
