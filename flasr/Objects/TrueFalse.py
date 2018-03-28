from .Question import Question

class TrueFalse(Question):

    def __init__(self, q_type, question):
        self.q_type = q_type
        self.question = question

    def getQuestion(self):
        return self.question

