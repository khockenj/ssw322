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
        title = document['title']
        listOfNames.append(title)
    return listOfNames

def load_survey(title, db, col):
    serialized_survey = col.find_one({"title": title})
    serialized_questions = serialized_survey['questions']
    survey = pickle.loads(serialized_survey['Survey'])
    survey.questions = []
    survey_answers = serialized_survey['answers']

    for c in range(len(serialized_questions)):
        survey.addQuestion(pickle.loads(serialized_questions[c]))
        survey.addAnswer(survey_answers[c])

    return(survey)
