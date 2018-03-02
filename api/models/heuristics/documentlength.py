from models.heuristic import Heuristic
from readcalc import readcalc

# Formal 4
# Ensure reasonable document length for target user
class DocumentLength(Heuristic):
    def score(self, eula):
        text = eula.text
        calc = readcalc.ReadCalc(text)
        words = len(calc.get_words())

        if words < 1200:
            score = 4
        elif words < 1700:
            score = 3
        elif words < 2000:
            score = 2
        elif words < 2500:
            score = 1
        else:
            score = 0

        #The tool will assign a grade of F for EULAs exceeding 2,500 words, D for 2,000 to 2,499 words,
        # C for 1,700 to 1,999 words, B for 1,200 to 1,699 words, and A for fewer than 1,200 words.

        return {'score': score, 'max': 4, 'numwords': words}
