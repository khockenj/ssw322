from .Question import Question

class Ranking(Question):

    options = None

    def __init__(self, q_type, question, choices=[]):
        self.q_type = q_type
        self.question = question
        self.choices = choices

    def addChoice(self, option):
        self.choices.append(option)

    def getChoices(self):
        return self.choices
