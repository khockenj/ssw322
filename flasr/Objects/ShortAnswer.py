from .Question import Question

class ShortAnswer(Question):

    def __init__(self, uniqueID, question, response):
        self.uniqueID = uniqueID
        self.question = question

    """def serialize(self):
    	response = {
    	    'uniqueID': self.uniqueID,
    	    'Question': self.question
    	}

    	return response
"""