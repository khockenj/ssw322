
class AnswerSheet:
    user_response = []
    title = "Error: No title found"
    userName = "User 1"

    def __init__(self, title):
        self.user_response = []
        self.title = title

    def addResponse(self, response):
        self.user_response.append(response)

    def getAnswers():
        return user_response
