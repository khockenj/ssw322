import pickle
from pymongo import MongoClient

def load_survey(name, db, col):
    serialized_survey = col.find_one({"name": name})
    survey = pickle.loads(serialized_survey)
