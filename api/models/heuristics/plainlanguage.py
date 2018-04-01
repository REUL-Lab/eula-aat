from models.heuristic import Heuristic
from readcalc import readcalc

class PlainLanguage(Heuristic):
    def score(self, eula):

        text = eula.text
        name = 'Plain Language'
        description = ['This heuristic checks the reading level of the EULA']
        grade = 'NR'
        max = 4

        calc = readcalc.ReadCalc(text)
        rl = calc.get_flesch_kincaid_grade_level()

        if rl < 8:
            score = 4
            grade = 'A'
        elif rl < 10:
            score = 3
            grade = 'B'
        elif rl < 12:
            score = 2
            grade = 'C'
        else:
            score = 0
            grade = 'F'

        return {
                'name' : name,
                'description' : description,
                'grade' : grade,
                'score': score,
                'max': 4,
                'readinglevel': rl
        }
