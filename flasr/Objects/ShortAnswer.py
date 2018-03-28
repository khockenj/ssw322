from .Question import Question

class ShortAnswer(Question):

    def __init__(self, q_type, question, charLimit):
        self.q_type = q_type
        self.question = question
        self.charLimit = charLimit
