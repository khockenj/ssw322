"""Main Survey Object"""

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
    	return questions
	