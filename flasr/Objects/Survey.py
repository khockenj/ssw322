"""Main Survey Object"""

class Survey:
    isTest = False
    answers = []
    questions = []
    name = 'Error: No name was assigned to the survey object'

    def __init__(self, isTest):
        self.isTest = isTest

    def addQuestion(self, questionID):
        self.questions.append(questionID)

    def addAnswer(self, answer):
        if self.isTest:
            self.answers.append(answer)

    def getQuestionList(self):
        return self.questions
