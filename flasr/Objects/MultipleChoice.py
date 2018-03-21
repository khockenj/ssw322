import Question from Question

class MultipleChoice(Question):

    choices = []

    def MultipleChoice(uniqueID, question, choices):
        self.uniqueID = uniqueID
        self.question = question
        self.choices = choices

    def getChoices:
        return choices
