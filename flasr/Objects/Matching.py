from .Question import Question

class Matching(Question):
    def __init__(self, q_type, question, choices=[], matches=[]):
        self.q_type = q_type
        self.question = question
        self.choices = choices
        self.matches = matches

    def addChoiceAndMatch(self, choice, Match):
        self.choices.append(choice)

    def getChoices(self):
        return self.choices
