from .Question import Question

class Matching(Question):

    def __init__(self, q_type, question, choices=[], matches=[]):
        self.q_type = q_type
        self.question = question
        self.choices = choices
        self.matches = matches

    def addChoiceAndMatch(self, choice, match):
        self.choices.append(choice)
        self.matches.append(match)
    def getChoices(self):
        return self.choices

    def getMatches(self):
        return self.matches
