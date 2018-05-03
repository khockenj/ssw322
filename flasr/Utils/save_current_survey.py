import pickle
import copy
from pymongo import MongoClient

def save_current_survey(current_survey, db, col):
    serialized_survey = pickle.dumps(current_survey)
    questions = []

    if col.find_one({'title': current_survey.title}):
        print("\n\n\n\n\n\n\n\n\n" + current_survey.title)
        col.delete_one({'title': current_survey.title})

    for question in current_survey.questions:
        questions.append(pickle.dumps(question))

    col.insert_one({'title': current_survey.title,
                    'Survey': serialized_survey,
                    'questions': questions,
                    'answers': current_survey.answers})
