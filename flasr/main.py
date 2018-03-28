import datetime
import sqlite3 as sql
import json
from math import pi
from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = bcrypt.hash("7f58dcac5fedb47467d61bf0f21de582")
sqlitedb = 'ssw322.db'

@app.route('/')
def index():
	logCheck = 0
	sid = session.get('uid');	#session if logged in
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
	email = request.form.get('email')	#form getters from post
	password1 = request.form.get('pass')
	fn = request.form.get('fn')
	ln = request.form.get('ln')
	try:
		dbconn = sql.connect(sqlitedb)
		dbconn.text_factory = str
		c = dbconn.cursor()
		sel = c.execute("SELECT * FROM `users` WHERE `email` = ? ", (email,))
		finder = c.fetchone()
		eCheck = validate_email(email)	#validates email, could do it myself but originally this library was supposed to send a message to the email server to check if the email is real
		email = eCheck['email']
		if session.get('uid'):	#session already set
			final = "You are already logged in."
		elif finder:	#email already in db
			final = "An account with that email already exists."
		elif eCheck == EmailNotValidError:	#email form isn't an email
			final = EmailNotValidError
		else:	#good to go
			hashedPass = bcrypt.hash(password1)	#hash bcrypt using secret key on top
			final = "registered"
			insertU = c.execute("INSERT INTO `users` (email, fn, ln, pass) VALUES (?, ?, ?, ?)", (email, fn, ln, hashedPass))	#insert into DB
			dbconn.commit()
		dbconn.close()
	except:
		final = "EXCEPTION: Couldn't connect to the database. Please reload."

	return final
@app.route('/login', methods=['POST'])
def login():
	final = "Couldn't connect to the database. Please reload."
	email = request.form.get('email')	#email/pw post
	password = request.form.get('pass')
	try:
		dbconn = sql.connect(sqlitedb)
		dbconn.text_factory = str
		c = dbconn.cursor()
		sel = c.execute("SELECT * FROM `users` WHERE `email` = (?) ", (email,))
		finder = sel.fetchone()
		if session.get('uid'):	#session already set
			final = "You are already logged in."
		elif not finder:	#email not found
			final = "Sorry, that E-mail doesn't exist."
		elif not bcrypt.verify(password, finder[4]):	#not correct password
			final = "Sorry, that is the wrong password."
		elif bcrypt.verify(password, finder[4]) and finder:	#probably doublelogic somewhere here but just in case, logged in
			final = "logged"
			session['uid'] = finder[0]	#set session
		else:
			final = "An unexpected error occurred. Please try again."
		dbconn.close()
	except:
		final = "ERROR: Couldn't connect to the database. Please reload."

	return final

@app.route('/logout')
def logout():
	final = ""
	session.pop('uid', None)	#pop that session out of here
	return final

@app.route('/dash')
def dashboard():
	logCheck = 0
	sid = session.get('uid');	#session if logged in
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

@app.route('/addToDB', methods=['POST'])
def addToDB():
	q = request.form.get('q')
	t = request.form.get('t')
	qType = request.form.get('qType')
	if qType == "mc":
		a = request.form.get('a')
		aChoices = request.form.get('ac')
	elif qType == "sa":
		climit = request.form.get('limit')
	elif qType == "r":
		placeholder = 0
		a = request.form.get('a')
	elif qType == "tf":
		placeholder = 0
		a = request.form.get('a')
	elif qType == "m":
		placeholder = 0
		a = request.form.get('a')
	else:
		q = "ERROR"
	
	return "q:" + q
	
@app.route('/edit')
def edit():
	return 0
@app.route('/take')
def take():
	return 0

	