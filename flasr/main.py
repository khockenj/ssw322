import datetime
import sqlite3 as sql
import json
import pickle
from math import pi
from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from werkzeug.contrib.cache import SimpleCache


#Project Imports
from Utils.load_survey import load_survey, get_titles
from Utils.save_current_survey import save_current_survey
from Utils.answer_sheet_to_db import answer_sheet_to_db
from Objects.Survey import Survey
from Objects.Question import Question
from Objects.Matching import Matching
from Objects.Ranking import Ranking
from Objects.TrueFalse import TrueFalse
from Objects.MultipleChoice import MultipleChoice
from Objects.ShortAnswer import ShortAnswer
from Objects.AnswerSheet import AnswerSheet
from Objects import current_survey, current_answer_sheet, cached_surveys, survey_num

#Database Setup
cache = SimpleCache()
client = MongoClient('localhost', 27017)
db = client['objects-database']
survey_col = db.survey_list
taker_col = db.taker_list
name_col = db.name_list

#Flask Setup
app = Flask(__name__)
app.secret_key = bcrypt.hash("7f58dcac5fedb47467d61bf0f21de582")
sqlitedb = 'ssw322.db'

@app.route('/')
def index():
    logCheck = 0
    sid = session.get('uid')   #session if logged in
    if sid:
        logCheck = sid
        return redirect(url_for('dashboard'))
    else:
        logCheck = 0
    #try:
        #if sid:
        #login stuff here
    #except:
        #test = "DB Connection Failure"
    return render_template('index.html', name='index', logcheck=logCheck)

@app.route('/register', methods=['POST'])
def register():
    final = "Couldn't connect to the database. Please reload"
    email = request.form.get('email')   #form getters from post
    password1 = request.form.get('pass')
    fn = request.form.get('fn')
    ln = request.form.get('ln')
    try:
        dbconn = sql.connect(sqlitedb)
        dbconn.text_factory = str
        c = dbconn.cursor()
        sel = c.execute("SELECT * FROM `users` WHERE `email` = ? ", (email,))
        finder = c.fetchone()
        eCheck = validate_email(email)  #validates email, could do it myself but originally this library was supposed to send a message to the email server to check if the email is real
        email = eCheck['email']
        if session.get('uid'):  #session already set
            final = "You are already logged in."
        elif finder:    #email already in db
            final = "An account with that email already exists."
        elif eCheck == EmailNotValidError:  #email form isn't an email
            final = EmailNotValidError
        else:   #good to go
            hashedPass = bcrypt.hash(password1) #hash bcrypt using secret key on top
            final = "registered"
            insertU = c.execute("INSERT INTO `users` (email, fn, ln, pass) VALUES (?, ?, ?, ?)", (email, fn, ln, hashedPass))   #insert into DB
            dbconn.commit()
        dbconn.close()
    except:
        final = "EXCEPTION: Couldn't connect to the database. Please reload."

    return final
@app.route('/login', methods=['POST'])
def login():
    final = "Couldn't connect to the database. Please reload."
    email = request.form.get('email')   #email/pw post
    password = request.form.get('pass')
    try:
        dbconn = sql.connect(sqlitedb)
        dbconn.text_factory = str
        c = dbconn.cursor()
        sel = c.execute("SELECT * FROM `users` WHERE `email` = (?) ", (email,))
        finder = sel.fetchone()
        if session.get('uid'):  #session already set
            final = "You are already logged in."
        elif not finder:    #email not found
            final = "Sorry, that E-mail doesn't exist."
        elif not bcrypt.verify(password, finder[4]):    #not correct password
            final = "Sorry, that is the wrong password."
        elif bcrypt.verify(password, finder[4]) and finder: #probably doublelogic somewhere here but just in case, logged in
            final = "logged"
            session['uid'] = finder[0]  #set session
        else:
            final = "An unexpected error occurred. Please try again."
        dbconn.close()
    except:
        final = "ERROR: Couldn't connect to the database. Please reload."

    return final

@app.route('/logout')
def logout():
    final = ""
    session.pop('uid', None)    #pop that session out of here
    return final

@app.route('/dash')
def dashboard():
    logCheck = 0
    sid = session.get('uid');   #session if logged in
    if sid:
        logCheck = sid
    else:
        logCheck = 0
    titles = get_titles(db, survey_col)
    return render_template('dashboard.html', name='dash', logcheck=logCheck, title=titles)

@app.route('/add', methods=['POST'])
def add():
    if current_survey.isTest == True:
        t = 't'
    else:
        t = 's'
    q = request.form.get('qType')
    return render_template('question.html', testOrSurvey=t, qType=q)

@app.route('/createSurveyObject', methods=['GET', 'POST'])
def createSurveyObject():
    t = request.form.get('t')

    global current_survey
    if t == 't':
        current_survey = None
        current_survey = Survey(True)
    else:
        current_survey = None
        current_survey = Survey(False)
    return t

@app.route('/saveSurvey', methods=['POST'])
def saveSurvey():
    global cached_surveys
    global current_survey
    current_survey.title = request.form.get('title')
    save_current_survey(current_survey, db, survey_col)
    return "saved to cache"

@app.route('/addToDB', methods=['POST'])
def addToDB():
    global current_survey
    current_question = None
    q = request.form.get('q')
    t = current_survey.isTest
    qType = request.form.get('qType')

    if qType == "mc":
        current_question = MultipleChoice("mc", q, choices = [])

        for c in range(1, int(request.form.get('n')) + 1):
            print(request.form.get('a' + str(c)))
            current_question.addChoice(request.form.get('a' + str(c)))

        if t == True:
            current_survey.addAnswer(request.form.get('c'))
    elif qType == "sa":
        climit = request.form.get('limit')
        current_question = ShortAnswer('sa', q, climit)
        if t == True:
            current_survey.addAnswer(" ")
    elif qType == "r":
        current_question = Ranking("r", q, choices = [])
        answer = []

        for c in range(1, int(request.form.get('n')) + 1):
            current_question.addChoice(request.form.get('a' + str(c)))
            if t == True:
                answer.append(request.form.get('r' + str(c)))
        if t == True:
            current_survey.addAnswer(answer)
    elif qType == "tf":
        current_question = TrueFalse("tf", q)

        if t == True:
            current_survey.addAnswer(request.form.get('opt'))
    elif qType == "m":
        current_question = Matching("m", q, choices = [], matches = [])
        for c in range(1, int(request.form.get('n')) + 1):
            current_question.addChoiceAndMatch(request.form.get('a' + str(c)), request.form.get('m' + str(c)))

        if t == True:
            current_survey.addAnswer(" ")
    else:
        q = "ERROR"

    current_survey.addQuestion(current_question)

    if t == True:
        return 't'
    else:
        return 's'

@app.route('/take/<int:qIndex>', methods=['GET', 'POST'])
def take(qIndex):
    global current_survey
    global current_answer_sheet

    title = current_survey.title
    if qIndex == 0:
        current_answer_sheet = AnswerSheet(title)

    if qIndex == None:
        someIndex = 0
    else:
        someIndex = qIndex

    qList = current_survey.getQuestionList()
    qLength = len(qList)
    aList = current_survey.answers
    counterForaList = 0

    question = ""
    choices = None
    matches = None
    options = None
    qType = None
    limit = 0

    i = qList[someIndex]
    question = i.question
    qType = i.q_type
    if i.q_type == "r" or i.q_type == "mc":
        choices = i.choices
    elif i.q_type == "sa":
        limit = i.charLimit
    elif i.q_type == "m":
        choices = i.choices
        matches = i.matches
    return render_template('take.html', climit = limit, passedQType = qType, passedQ = question, passedChoices = choices, passedMatches = matches, qIndex = someIndex, length = qLength)

@app.route('/saveAnswer', methods=['POST'])
def saveAnswer():
    global current_answer_sheet

    qType = request.form.get('qType')
    if qType == 'r' or qType == 'm':
        a = request.values.getlist('a[]')
        current_answer_sheet.addResponse(a)
    elif qType == 'sa':
        current_answer_sheet.addResponse('SA')
    else:
        current_answer_sheet.addResponse(request.form.get('a'))
    return "Return: " + str(request.values.getlist('a[]'))

@app.route('/storeToAnswerSheet', methods=['POST', 'GET'])
def storeToAnswerSheet():
    global current_answer_sheet
    correct = []
    current_answer_sheet.title = current_survey.title
    current_answer_sheet.userName = session.get('uid')
    answer_sheet_to_db(current_answer_sheet, db, taker_col)

    for index, answer in enumerate(current_survey.answers):
        #print('\n\n\n' + str(answer) + '\n\n\n')
        if answer == current_answer_sheet.user_response[index]:
            correct.append('Correct')
        elif current_answer_sheet.user_response[index] == 'SA':
            correct.append('SA')
        else:
            correct.append('Incorrect')

    print('\n\n\n' + str(correct) + '\n\n\n')

    return render_template('grade.html', correct = correct)



@app.route('/edit/<int:qIndex>', methods=['GET', 'POST'])
def edit(qIndex):
    global current_survey
    question = ""

    choices = None
    matches = None
    options = None
    qType = None
    limit = 0
    ans = None

    title = current_survey.title

    if qIndex == None:
        someIndex = 0
    else:
        someIndex = qIndex

    if len(current_survey.getQuestionList()) == qIndex:
        current_surveys.addQuestion(Question())
        current_surveys.addAnswer(None)
        return render_template('edit.html', climit = limit, passedQType = qType, passedQ = question, passedChoices = choices, passedMatches = matches, qIndex = someIndex, length = qLength, passedAns = ans)

    qList = current_survey.getQuestionList()
    qLength = len(qList)
    aList = current_survey.answers

    if current_survey.isTest:
        ans = aList[qIndex]

    i = qList[someIndex]
    question = i.question
    qType = i.q_type
    if i.q_type == "r" or i.q_type == "mc":
        choices = i.choices
    elif i.q_type == "sa":
        limit = i.charLimit
    elif i.q_type == "m":
        choices = i.choices
        matches = i.matches
    return render_template('edit.html', climit = limit, passedQType = qType, passedQ = question, passedChoices = choices, passedMatches = matches, qIndex = someIndex, length = qLength, passedAns = ans)


@app.route('/changeQuestion', methods=['GET', 'POST'])
def changeQuestion():
    global current_survey
    current_question = None
    q = request.form.get('q')
    t = current_survey.isTest
    n = int(request.form.get('qIndex'))
    qType = request.form.get('qType')

    if qType == "mc":
        current_question = MultipleChoice("mc", q, choices = [])

        for c in range(1, int(request.form.get('n')) + 1):
            current_question.addChoice(request.form.get('a' + str(c)))

        if t == True:
            current_survey.answers[n] = request.form.get('c')
    elif qType == "sa":
        climit = request.form.get('limit')
        current_question = ShortAnswer('sa', q, climit)
        if t == True:
            current_survey.answers[n] = " "
    elif qType == "r":
        current_question = Ranking("r", q)
        answer = []

        for c in range(1, int(request.form.get('n')) + 1):
            current_question.addChoice(request.form.get('r' + str(c)))
            if t == True:
                answer.append(request.form.get('a' + str(c)))
        if t == True:
            current_survey.answers[n] = answer
    elif qType == "tf":
        current_question = TrueFalse("tf", q)

        if t == True:
            current_survey.answers[n] = request.form.get('opt')
    elif qType == "m":
        current_question = Matching("m", q)
        for c in range(1, int(request.form.get('n')) + 1):
            current_question.addChoiceAndMatch(request.form.get('a' + str(c)), request.form.get('m' + str(c)))

        if t == True:
            current_survey.answers[n] = " "
    else:
        q = "ERROR"

    current_survey.questions[n] = current_question

    return "q:" + qType

@app.route('/loadSurvey', methods=['POST'])
def loadSurvey():
    global current_survey
    current_survey = None
    selected = request.form.get('selected')

    current_survey = load_survey(selected, db, survey_col)
    return " "

@app.route('/view/<int:qIndex>', methods=['GET', 'POST'])
def view(qIndex):
    """survey = Survey(True)
    survey.addQuestion(Matching("M", "This is the Question.", ["option1", "option2", "option3"], ["option1", "option2", "option3"]))
    survey.addAnswer("Matching got no answer.")
    survey.addQuestion(MultipleChoice("MC", "This is the question", ["option1", "option2", "option3"]))
    survey.addAnswer(1)
    survey.addQuestion(Ranking("R", "This is the question", ["option1", "option2", "option3"]))
    survey.addAnswer([1,2,3])
    survey.addQuestion(ShortAnswer("SA", "This is the question", 52))
    survey.addAnswer(" ")
    survey.addQuestion(TrueFalse("TF", "This is the question",))
    survey.addAnswer(0)"""

    global current_survey
    if qIndex == None:
        someIndex = 0
    else:
        someIndex = qIndex

    survey = current_survey
    qList = survey.getQuestionList()
    qLength = len(qList)
    aList = survey.answers
    counterForaList = 0

    question = ""
    answer = ""
    choices = None
    matches = None
    options = None
    qType = None
    characters = 0

    i = qList[someIndex]
    question = i.question
    qType = i.q_type
    if i.q_type == "r":
        choices = i.choices
    elif i.q_type == "mc":
        choices = i.choices
    elif i.q_type == "m":
        choices = i.choices
        matches = i.matches
    elif i.q_type == "sa":
        characters = i.charLimit
    else:
        answer = ""

    if survey.isTest:
        if i.q_type == "tf" or i.q_type == "r" or i.q_type == "mc" or i.q_type == "sa":
            answer = aList[someIndex]
        else:
            answer = " "

    return render_template('view.html', climit = characters, passedQType = qType, passedQ = question, passedAns = answer, passedChoices = choices, passedMatches = matches, qIndex = someIndex, length = qLength)
