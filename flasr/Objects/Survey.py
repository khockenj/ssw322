"""Main Survey Object"""
from .

class Survey:
	isTest = False
	answers = []
    questions = []

    def __init__(self, isTest):
        self.isTest = isTest

    def addQuestion(questionID, answer=None):
    	questions.append(questionID)

        if isTest and answer:
            answers.append(answer)

    def getQuestionList:
    	return self.questions

   """ def serialize(self):
        response = {
            'isTest': self.isTest,
            'Answers': self.Answers,
            'Questions': []
        }
        for c in self.questions:
            response['Questions'].append(c.serialize())

        return response
"""