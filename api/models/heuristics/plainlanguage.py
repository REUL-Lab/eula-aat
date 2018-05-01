from models.heuristic import Heuristic
from readcalc import readcalc

class PlainLanguage(Heuristic):

    @staticmethod
    def score(eula):
        text = eula.text
        name = 'Plain Language'
        description = 'Checks the reading level of the EULA (K-12)'
        grade = 'NR'
        max = 4

        calc = readcalc.ReadCalc(text)
        rl = calc.get_flesch_kincaid_grade_level()

        feedback = []

        if rl < 8:
            score = 4
            grade = 'A'
            feedback.append({'rating': 2, 'text': "Your EULA has a reading level of {0:.0f}".format(rl)})
        elif rl < 10:
            score = 3
            grade = 'B'
            feedback.append({'rating': 2, 'text': "Your EULA has a reading level of {0:.0f}".format(rl)})
        elif rl < 12:
            score = 2
            grade = 'C'
            feedback.append({'rating': 1, 'text': "Your EULA has a reading level of {0:.0f}".format(rl)})
        else:
            score = 0
            grade = 'F'
            feedback.append({'rating': 0, 'text': "Your EULA has a reading level of {0:.0f}".format(rl)})

        feedback.append({'rating': 3, 'text': 'The average American has a reading level of grade 8'})

        return {
            'name' : name,
            'description' : description,
            'grade' : grade,
            'score': score,
            'max': 4,
            'feedback': feedback
        }
