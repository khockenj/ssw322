import datetime
import sqlite3 as sql
import json
from math import pi
from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from werkzeug.contrib.cache import SimpleCache


#Project Imports
from Objects.Survey import Survey
from Objects.Question import Question
from Objects.Matching import Matching
from Objects.Ranking import Ranking
from Objects.TrueFalse import TrueFalse
from Objects.MultipleChoice import MultipleChoice
from Objects.ShortAnswer import ShortAnswer

from Objects import current_survey, cached_surveys, survey_num
#Database Setup
cache = SimpleCache()
client = MongoClient('localhost', 40000)
db = client['objects-database']

#Flask Setup
app = Flask(__name__)
app.secret_key = bcrypt.hash("7f58dcac5fedb47467d61bf0f21de582")
sqlitedb = 'ssw322.db'

@app.route('/')
def index():
    logCheck = 0
    sid = session.get('uid');   #session if logged in
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
    return render_template('dashboard.html', name='dash', logcheck=logCheck)

@app.route('/add', methods=['POST'])
def add():
    t = request.form.get('t')
    q = request.form.get('qType')
    return render_template('question.html', testOrSurvey=t, qType=q)

@app.route('/createSurveyObject', methods=['POST'])
def createSurveyObject():
    t = request.form.get('t')
    global current_survey
    if t == 't':
        current_survey = Survey(True)
        return('Test')
    else:
        current_survey = Survey(False)
        return(str(current_survey.isTest))
    return t



@app.route('/addToDB', methods=['POST'])
def addToDB():
    global current_survey
    current_question = Question()
    q = request.form.get('q')
    t = request.form.get('t')
    qType = request.form.get('qType')

    if qType == "mc":
        current_question = MultipleChoice("MC", q)
        try:
            count = 1
            while(True):
                current_question.addChoice(request.form.get('a' + str(count)))
                count += 1
        finally:
            current_survey.addAnswer(request.form.get('c'))
    elif qType == "sa":
        climit = request.form.get('limit')
        current_question = ShortAnswer('SA', q, climit)
    elif qType == "r":
        current_question = Ranking("R", q)
        answer = []
        try:
            count = 1
            while(True):
                current_question.addOption(request.form.get('r' + str(count)))
                answer.append(request.form.get('a' + str(count)))
                count += 1
        finally:
            current_survey.addAnswer(answer)
    elif qType == "tf":
        current_question = TrueFalse("TF", q)
        current_survey.addAnswer(request.form.get('opt'))
    elif qType == "m":
        current_question = Matching("M", q)
        try:
            count = 1
            while(True):
                current_question.addChoiceAndMatch(request.form.get('a' + str(count)), request.form.get('m' + str(count)))
                count += 1
        finally:
            print("get right wit ya")
    else:
        q = "ERROR"

    current_survey.addQuestion(current_question)

    return "q:" + q

@app.route('/edit')
def edit():
    return 0
@app.route('/take')
def take():
    return 0

@app.route('/view')
def view():
	survey = Survey(True)
	survey.addQuestion(Matching("M", "This is the Question.", ["option1", "option2", "option3"], ["option1", "option2", "option3"]))
	survey.addAnswer("Matching got no answer.")
	survey.addQuestion(MultipleChoice("MC", "This is the question", ["option1", "option2", "option3"]))
	survey.addAnswer(1)
	survey.addQuestion(Ranking("R", "This is the question", ["option1", "option2", "option3"]))
	survey.addAnswer([1,2,3])
	survey.addQuestion(ShortAnswer("SA", "This is the question", 52))
	survey.addAnswer(" ")
	survey.addQuestion(TrueFalse("TF", "This is the question",))
	survey.addAnswer(0)

	qList = survey.getQuestionList()
	aList = survey.answers
	counterForaList = 0

	question = ""
	answer = ""
	choices = None
	matches = None
	options = None
	qType = None

	for i in qList:
		question = i.question
		qType = i.q_type
		if i.q_type == "TF":
			answer = aList[counterForaList]
		elif i.q_type == "SA":
			answer = None
		elif i.q_type == "R":
			answer = aList[counterForaList]
			options = i.options
		elif i.q_type == "MC":
			answer = aList[counterForaList]
			choices = i.choices
		else:
			answer = aList[counterForaList]
			choices = i.choices
			matches = i.matches

	return render_template('view.html', passedQType = qType, passedQ = question, passedAns = answer, passedChoices = choices, passedMatches = matches)
