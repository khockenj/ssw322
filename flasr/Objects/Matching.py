from .Question import Question

class Matching(Question):
    choices = []

    def __init__(self, q_type, question, choices):
        self.q_type = q_type
        self.question = question
        self.choices = choices

    def addChoice(self, choice):
        self.choices.append(choice)

    def getChoices():
        return choices
