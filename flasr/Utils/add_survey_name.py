import pickle

from pymongo import MongoClient

def add_survey_name(current_survey, col):
    survey_names = col.find_one()
    survey_names = pickle.loads(survey_names)

    if not(current_survey.title in survey_names):
    	survey_names.append(current_survey.title)

    col.replace_one()