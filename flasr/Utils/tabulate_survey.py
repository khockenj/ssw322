from pymongo import MongoClient

from Objects.AnswerSheet import AnswerSheet
from Objects.Survey import Survey
from Objects.Question import Question

def tabulate_survey(db, survey_col, taker_col, survey_to_tabulate):
    list_of_titles = get_titles(db, survey_col)
    list_of_survey_titles = []
    list_of_answer_sheet_responses = []
    list_of_survey_questions = []

    times_chosen = 0
    list_of_times_for_each_question = []

    #Stores a list of just the survey titles for the survey to be tabulated
    for title in list_of_titles:
        a_test_or_surv = load_survey(title, db, survey_col)
        if a_test_or_surv.isTest == False and a_test_or_surv.title == 'survey_to_tabulate':
            #Stores a list of answer sheet user_response lists for the corresponsing surveys
            answer_sheet = load_answer_sheet(title, db, taker_col)
            list_of_answer_sheet_responses.append(answer_sheet.user_response)
            #Store the list of survey questions
            list_of_survey_questions = a_test_or_surv.questions

            for q_index, question in list_of_survey_questions:
                #tf = [T, F]
                tf = []
                for response_list in list_of_answer_sheet_responses:
                    response_to_current_question = response_list[q_index]
                    if question.q_type == 'tf':
                        tf = tabulate_tf(response_to_current_question, tf)


def tabulate_tf(response_to_current_question, tf):
    if response_to_current_question == 1:
        tf[0] +=1
    else:
        tf[1] += 1

    return tf
