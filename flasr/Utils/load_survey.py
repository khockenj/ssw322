import pickle

from pymongo import MongoClient

from Objects.Survey import Survey
from Objects.Question import Question
from Objects.Matching import Matching
from Objects.Ranking import Ranking
from Objects.TrueFalse import TrueFalse
from Objects.MultipleChoice import MultipleChoice
from Objects.ShortAnswer import ShortAnswer

def get_titles(db, col):
	listOfNames = []
	for document in col.find():
		name = document.name
		listOfNames.append(name)
	print(listOfNames)
	return listOfNames

def load_survey(name, db, col):
	serialized_survey = col.find_one({"name": name})
	survey_dict = pickle.loads(serialized_survey)
	questions = survey_dict.questions
	survey = Survey(survey_dict.isTest)
	survey.name = name
	if survey.isTest == True:
		survey.answers = survey_dict.answers

	for c in range(len(questions)):
		survey.addQuestion(create_question(survey, survey_dict.questions[c], survey_dict.isTest))

	return(survey)


def create_question(survey, question, isTest):
	if question.q_type == "MC":
		response = MultipleChoice("MC", question.question)

		for c in range(len(question.choices)):
			response.addChoice(question.choices[c])

	elif question.q_type == "SA":
		response = ShortAnswer('SA', question.question, question.charLimit)

	elif question.q_type == "R":
		response = Ranking("R", question.question)

		for c in range(len(question.choices)):
			response.addChoice(question.choices[c])

	elif question.q_type == "TF":
		response = TrueFalse("TF", question.question)

	elif question.q_type == "M":
		response = Matching("M", question.question)
		for c in range(len(question.choices)):
			response.addChoiceAndMatch(question.choices[c], question.matches[c])

	else:
		return None

	return response
