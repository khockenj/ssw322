from .Question import Question

class TrueFalse(Question):

    def __init__(self, uniqueID, question):
        self.uniqueID = uniqueID
        self.question = question

    def getQuesstion:
        return Question

    def serialize(self):
    	response = {
    	     'uniqueID': self.uniqueID,
    	     'Question': self.question
    	}
