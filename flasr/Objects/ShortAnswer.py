from .Question import Question

class ShortAnswer(Question):

    def __init__(self, uniqueID, question, charLimit):
        self.uniqueID = uniqueID
        self.question = question
        self.charLimit = charLimit

    """def serialize(self):
    	response = {
    	    'uniqueID': self.uniqueID,
    	    'Question': self.question
            'charLimit': self.charLimit
    	}

    	return response
"""
