"""Main Survey Object"""

class Survey:
    isTest = False
    answers = []
    questions = []

    def __init__(self, isTest):
        self.isTest = isTest

    def addQuestion(questionID):
        questions.append(questionID)

    def addAnswer(answer):
        if isTest:
            answers.append(answer)

    def getQuestionList():
        return self.questions
