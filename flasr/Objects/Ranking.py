from .Question import Question

class Ranking(Question):

    def __init__(self, q_type, question, options=[]):
        self.q_type = q_type
        self.question = question
        self.options = options

    def addOption(option):
        self.options.append(option)

    def getOptions():
        return options

