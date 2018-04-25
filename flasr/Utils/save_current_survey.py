import pickle
from pymongo import MongoClient

def save_current_survey(current_survey, db, col):
    serialized_survey = pickle.dumps(current_survey)
    print(serialized_survey)

    if col.find_one({'title': current_survey.title}):
        col.delete_one({'title': current_survey.title})

    col.insert_one({'title': current_survey.title,
                    'Survey': serialized_survey})
