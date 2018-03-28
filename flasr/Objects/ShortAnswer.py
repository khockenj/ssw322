from Question import Question

class ShortAnswer(Question):

    def __init__(self, uniqueID, question, response):
        self.uniqueID = uniqueID
        self.question = question
