from .Question import Question

class Ranking(Question):

    options = None

    def __init__(self, q_type, question, options=[]):
        self.q_type = q_type
        self.question = question
        self.options = options

    def addOption(self, option):
        self.options.append(option)

    def getOptions(self):
        return options
