""" This file should contain only a single class, EULA.  It is to be the object representation of a user-provided EULA
"""

class EULA:

    """Class for EULAs.  Both input methods should create a EULA object with the full set of instance variables.

    Args:
        text: the parsed text of the EULA, containing no formatting and ASCII format text only
        url: the URL of the EULA (if applicable)
        html: the html of the desktop session
        desk_driver: the selenium driver for the headless desktop instance
        mobile_driver: the selenium driver for the headless mobile instance

    """

    def __init__(self, text, url=None, title=None, html=None, driver=None, desk_driver=None, mobile_driver=None):
        self.text = text
        self.url = url
        self.html = html
        self.desk_driver = desk_driver
        self.mobile_driver = mobile_driver

        # Set title to page title and format for length.  URLs stay full length
        if title is not None and title is not '' and title is not ' ':
            if len(title) > 40:
                self.title = title[:37] + '...'
            else:
                self.title = title
        else:
            self.title = url

