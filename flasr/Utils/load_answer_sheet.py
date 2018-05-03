import pickle

from pymongo import MongoClient

from Objects.AnswerSheet import AnswerSheet

def load_answer_sheet(title, db, taker_col):
    serialized_answer_sheet = taker_col.find_one({'Title': title})
    serialized_responses = serialized_survey['Responses']
    answer_sheet = pickle.loads(serialized_answer_sheet['AnswerSheet'])

    for response in serialized_responses:
        answer_sheet.addResponse(pickle.loads(response))

    return answer_sheet
