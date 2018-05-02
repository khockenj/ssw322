import pickle
import copy
from pymongo import MongoClient

def answer_sheet_to_db(current_answer_sheet, db, col):
    serialized_answer_sheet = pickle.dumps(current_answer_sheet)
    responses = []

    if col.find_one({'Title': current_answer_sheet.title, 'User': current_answer_sheet.userName}):

        for response in current_answer_sheet.user_response:
            responses.append(pickle.dumps(response))

        col.insert_one({'Title': current_answer_sheet.title, 'User': current_answer_sheet.userName, 'AnswerSheet': serialized_answer_sheet, 'Responses': responses})
