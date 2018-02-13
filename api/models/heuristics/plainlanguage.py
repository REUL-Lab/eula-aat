from models.heuristic import Heuristic
from readcalc import readcalc
import pyphen
import math

# Substantive 1a
# Incorporate plain language in EULA.
grades = {
  0: (lambda x: x > 12),               # F
  1: (lambda x: False),    # D
  2: (lambda x: x < 12 and x >= 10),    # C
  3: (lambda x: x < 10 and x >= 8),     # B
  4: (lambda x: x < 8)                  # A
}

class PlainLanguage(Heuristic):
    def __get_number_syllables(self, words):
        dic = pyphen.Pyphen(lang='en')

        syllables = 0
        words_3_syllables_more = 0

        for word in words:
            syl = len(dic.inserted(word).split("-"))
            syllables += syl
            if syl >= 3:
                words_3_syllables_more += 1
        return syllables, words_3_syllables_more



    def score(self, eula):

        text = eula.text

        calc = readcalc.ReadCalc(text)
        grade = calc.get_flesch_kincaid_grade_level()


        # TODO: Work on this metric
        # Flesch-kincaid works poorly on individual sentences because of the baseline additions.
        # Waiting on REUL lab response for how we should do this.
        failing_sentences = []
        for sentence in calc.get_sentences():
            # If sentence is failing, make sure it's hilighted
            if self.__get_number_syllables(sentence)[1] > 5 or len(list(sentence)) > 12:
                failing_sentences.append(sentence)

        calc_score = -1
        # Overall grade level is used for score
        for score, scorer in grades.iteritems():
            if scorer(grade):
                calc_score = score

        return {'score': calc_score, 'max': 4, 'readinglevel': grade, 'failing_sentences': failing_sentences }