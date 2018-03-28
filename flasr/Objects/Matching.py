from Question import Question

class Matching(Question):
    choices = []

    def __init__(self, uniqueID, question, choices):
        self.uniqueID = uniqueID
        self.question = question
        self.choices = choices

    def addChoice(self, choice):
        self.choices.append(choice)

    def getChoices:
        return choices

    def serialize():
    	response = {
    	    'uniqueID': self.uniqueID,
            'Question': self.question,
            'Choices': self.choices
    	}
    	return response