from .Question import Question

class ShortAnswer(Question):

    def __init__(self, uniqueID, question, charLimit):
        self.uniqueID = uniqueID
        self.question = question
        self.charLimit = charLimit
