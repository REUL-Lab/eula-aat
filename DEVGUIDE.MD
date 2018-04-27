# Expanding the Automated Analysis Tool

The EULA Automated Analysis tool was designed to allow maximum interoperability with new heuristics.  The following is a guide of how heuristics should be implemented, and then added to the processing engine.

## Developing a Heuristic

All heuristics are located in `api/models/heuristics/`.  They fit the form of the following code skeleton:

```from models.heuristic import Heuristic

class ExampleHeuristic(Heuristic):
    
    @staticmethod
    def score(eula):
        return {
            'name'       : name,
            'grade'      : grade,
            'description': description,
            'score'      : score,
            'max'        : 4
        }```

### Using the eula object
A `eula` object contains the following properties:
* `eula.text`: the extracted text contents of the EULA, omitting any style or non-legal language.

The following apply only to EULAs submitted via the "URL to EULA" option.  If a EULA was uploaded, the values of these variables will be `None`
* `eula.url`: the URL of the EULA.
* `eula.html`: the HTML contents of a EULA.  If the link to the document was not a web page (i.e. a pdf), this value will be `None`
* `eula.desk_driver`: A [Selenium-hooked Chrome WebDriver](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver) that allows interaction with the desktop page.  If the link to the document was not a web page (i.e. a pdf), this value will be `None`
* `eula.mobile_driver`: A [Selenium-hooked Chrome WebDriver](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver) but for the mobile page.

### Notes when Writing a Heuristic
All heuristics must implement the score method and have a return statement that includes a dictionary of the listed values.  Heuristics that do not return a score or max (maximum score) will not be counted, and heuristics that do not include a grade will be displayed incorrectly.

Heuristics are run in a threaded environment with built-in error handling.  If your heuristic encounters an error, the dispatcher will omit it from the return to the client and it will not be displayed.  You must check your console log for the error.  Take note that because the error occurs inside of a thread, the stack trace will be very long and need to view the top portion for information relevant to your code.

## Adding a Heuristic to the Dispatcher

Once your heuristic has been written, it must be added to the dispatcher in order to be run.  The dispatcher uses values in the `formal.py`, `procedural.py` and `substantive.py` files in the `api/models/categories/` directory.  Add the heuristic like follows

```def get_heuristics():
    return {
        mobileaccessibility.MobileAccessibility: 2,
        notifychangesinpolicy.NotifyChangesInPolicy: 3,
        mobilereadability.MobileReadability: 5,
        exampleheuristic.ExampleHeuristic: x
    }```

where `x` would be the value-relative weight for the heuristic.  These values do not have to be summed, but are used to weigh heuristics against one another when calculating the final score.  Ensure that you import your heuristic at the top of the file.