from models.heuristic import Heuristic
from nltk import tokenize
import re

# Ratios do not have to add to any number, but are relative to eachother
grade_ratios = {
    'caps': 5,
    'headings': 3,
    'serif': 1
}

# Caps grading is based on percentage of documents written in all caps
caps_grading = {
    0: (lambda x: x >= .5 and x < 1),   # Between 50% and 100% caps
    1: (lambda x: x >= .2 and x < .5),  # Between 20% and 50% caps
    4: (lambda x: x < .2)               # Less than 20% caps
}

# Human-feedback for caps grading
caps_humanized = {
    0: {'rating': 0, 'text': 'This EULA uses many uppercase words'},
    1: {'rating': 1, 'text': 'This EULA uses some uppercase words'},
    4: {'rating': 2, 'text': 'This EULA has few uppercase words'}
}

# Count of headings to consider in calculation (if it shows up less than this, don't count it)
headings_threshhold = 3
# Headings grading is based upon the relative frequency of the most common heading
headings_grading = {
    0: (lambda x: x >= 0 and x < 0.5),    # Very mixed headings
    2: (lambda x: x >= 0.5 and x < 0.7),  # Mixed headings
    4: (lambda x: x >= .7),               # Almost no mixed headings
}

# Human-feedback for heading
headings_humanized = {
    0: {'rating': 0, 'text': 'This EULA contains very mixed headings'},
    2: {'rating': 1, 'text': 'This EULA contains mixed headings'},
    4: {'rating': 2, 'text': 'This EULA has unified headings'}
}

#Human feedback for serif
serif_humanized = {
    True: {'rating': 0, 'text': 'This EULA uses a serif font'},
    False: {'rating': 2, 'text': 'This EULA does not use a serif font'}
}

# Formal 1
# Standardize type conventions throughout document for clarity.
class TypeConventions(Heuristic):

    @staticmethod
    def score(eula):
        name = 'Type Conventions'
        description = 'Analyzes the type conventions of the EULA'
        grade = 'NR'
        grades = ['F', 'D', 'C', 'B', 'A']
        feedback = []

        sentences = []
        # Remove sentences containing only punctuation:
        for sentence in tokenize.sent_tokenize(eula.text):
            if re.sub("\W", "", sentence):
                sentences.append(sentence)

        # Count the number of sentences which filter as uppercase
        caps_sentences = filter(lambda x: x.isupper(), sentences)
        # Convert to float before division to preserve decimal
        caps_ratio = float(len(caps_sentences)) / len(sentences)

        # Run the scorers and see which int grade to assign
        for x, caps_scorer in caps_grading.iteritems():
            if caps_scorer(caps_ratio):
                caps_score = x

        # Dict for caps embedding
        caps = {'caps_ratio': caps_ratio, 'all_caps_sentences': caps_sentences}

        # Add humanized caps to feedback
        feedback.append(caps_humanized[caps_score])

        # Headings score will be percent of most occuring headings
        headings_score = -1

        if eula.html is None:
            headings = 'N/A'
        else:
            # Different level heading tags to count
            heading_types = ['h1', 'h2', 'h3', 'h4', 'h5']
            # Count number of headings that occur
            headings_counts = dict((head, eula.html.count(head)) for head in heading_types)

            # Filter for headings that occur more often than the threshold
            common_headings = dict((head, headings_counts[head]) for head in \
                filter(lambda x: headings_counts[x] > headings_threshhold, headings_counts.keys()))

            # Convert to float in order to preserve decimal
            headings_ratio = float(max(common_headings.values())) / sum(common_headings.values())
            # Iterate over score and scorer in the grading dict defined at top
            for x, headings_scorer in headings_grading.iteritems():
                if headings_scorer(headings_ratio):
                    headings_score = x

            headings = {'counts': headings_counts, 'score': headings_score}
            feedback.append(headings_humanized[headings_score])

        if eula.desk_driver is None:
            serif = 'N/A'
        else:
            # Start as none in case we can't find it
            elements = None
            # Search for each sentence until we find one
            for sentence in sentences:
                # Find a sentence in the identified document that exists in the DOM
                search = (u"//*[contains(text(), '{0}')]").format(sentence)
                # Grab elements
                elements = eula.desk_driver.find_elements_by_xpath(search)
                # Found a sentence in the DOM
                if len(elements) > 0:
                    break

            # If not findable, don't take points off
            if elements is None or len(elements) == 0:
                serif = None
            else:
                # Found an element with an identifyable font
                font_family = elements[0].value_of_css_property('font-family')
                # Strip the family into pieces
                fonts = map(lambda x: x.lower().strip(), font_family.split(','))
                # Serif = "True" if in family string, "False" if not
                serif = 'serif' in fonts
                # Add serif to feedback
                feedback.append(serif_humanized[serif])

        # We always have the score for caps since it's in text.
        heur_numerator = caps_score * grade_ratios['caps']
        heur_denom = max(caps_grading.keys()) * grade_ratios['caps']

        # If we couldn't identify serif, don't detract from it
        heur_numerator = heur_numerator + (grade_ratios['serif'] if serif else 0)
        heur_denom = heur_denom + (grade_ratios['serif'] if serif is not None else 0)

        # If we couldn't identify headings, don't detract from it
        heur_numerator = heur_numerator + (headings_score * grade_ratios['headings'] if headings_score != -1 else 0)
        heur_denom = heur_denom + ((max(headings_grading.keys()) * grade_ratios['headings']) if headings_score != -1 else 0)

        # Set the score as an int in [0,4]
        # Convert numerator to float in order to preserve decimal for rounding
        heur_score = int(round(float(heur_numerator) * 4 / heur_denom))
        grade = grades[heur_score]

        return {
            'name' : name,
            'description' : description,
            'grade': grade,
            'score': heur_score,
            'max': 4,
            'feedback': feedback
        }
