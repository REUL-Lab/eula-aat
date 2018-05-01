from models.heuristic import Heuristic
from readcalc import readcalc

# Formal 4
# Ensure reasonable document length for target user
class DocumentLength(Heuristic):

    @staticmethod
    def score(eula):
        name = 'Document Length'
        text = eula.text
        calc = readcalc.ReadCalc(text)
        words = len(calc.get_words())
        description = 'Counts the number of words in the EULA'
        feedback = ['This EULA is {0} words long'.format(words)]

        if words < 1200:
            score = 4
            grade = 'A'
            feedback.append('This EULA is short and succinct')
        elif words < 1700:
            score = 3
            grade = 'B'
            feedback.append('This EULA is relatively concise')
        elif words < 2000:
            score = 2
            grade = 'C'
            feedback.append('This EULA is a bit long')
        elif words < 2500:
            score = 1
            grade = 'D'
            feedback.append('This EULA is very long')
        else:
            score = 0
            grade = 'F'
            feedback.append('This EULA is too long')

        #The tool will assign a grade of F for EULAs exceeding 2,500 words, D for 2,000 to 2,499 words,
        # C for 1,700 to 1,999 words, B for 1,200 to 1,699 words, and A for fewer than 1,200 words.

        return {
            'name'       : name,
            'grade'      : grade,
            'description': description,
            'feedback'   : feedback,
            'score'      : score,
            'max'        : 4,
            'numwords'   : words
        }
