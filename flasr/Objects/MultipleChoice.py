from Question import Question

class MultipleChoice(Question):

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
    	    'uniquID': uniqueID,
            'Question': question,
            'choices': choices
    	}
    	return response
