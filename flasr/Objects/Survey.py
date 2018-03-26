"""Main Survey Object"""

class Survey:
	isTest = False
	answers = []
    questions = []

    def Survey(isTest):
        self.isTest = isTest

    def addQuestion(question, answer=None):
    	questions.append(question)

        if isTest and answer:
            answers.append(answer)

    def getQuestionList:
    	return questions
	