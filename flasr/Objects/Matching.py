from Question import Question

class Matching(Question):
    choices = []

    def __init__(self, uniqueID, question, choices):
        self.uniqueID = uniqueID
        self.question = question
        self.choices = choices

    def getChoices:
        return choices
