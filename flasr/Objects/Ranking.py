from .Question import Question

class Ranking(Question):
    options = []

    def __init__(self, uniqueID, question, options):
        self.uniqueID = uniqueID
        self.question = question
        self.options = options

    def addOption(option):
        self.options.append(option)

    def getOptions():
        return options

