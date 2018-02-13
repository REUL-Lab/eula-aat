""" This file should contain only a single class, EULA.  It is to be the object representation of a user-provided EULA
"""

import category, substantive

class EULA:

    """Class for EULAs.  Both input methods should create a EULA object with the full set of instance variables.

    A EULA

    Note:
        The page of a EULA should be done inside of this class.  The input sources should only provide the URL/File.

    Args:
        URL: the accessible URL for a EULA.  If the user uploads a PDF, this should be the temp stored html-ized version of that PDF

    Attributes:
        URL: the URL passed in during the constructor
        text: the parsed text of the EULA, containing no formatting and ASCII format text only
        render: the page rendered via chrome-headless

    """

    def __init__(self, text, html=None, desktop_render=None, mobile_render=None):
        self.text = text
        self.html = html
        self.desktop_render = desktop_render
        self.mobile_render = mobile_render