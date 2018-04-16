import pickle
from pymongo import MongoClient

def save_current_survey(current_survey, db, col):
    serialized_survey = pickle.dumps(current_survey)
    col.insert_one(serialized_survey)
