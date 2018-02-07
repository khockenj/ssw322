import datetime
import sqlite3 as sql
import json
from math import pi
import pandas as pd
import feedparser as fp
from bokeh.plotting import figure
from bokeh.charts import Horizon, output_file, show
from bokeh.embed import file_html
import bokeh.models
from validate_email import validate_email
from passlib.hash import bcrypt
from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = bcrypt.hash("2pacisalive")
sqlitedb = 'ssw322.db'

@app.route('/')
def index():
	logCheck = 0
	sid = session.get('uid');	#session if logged in
	if sid:
		logCheck = sid
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
	email = request.form.get('email')	#form getters from post email/pw
	password1 = request.form.get('pw1')
	try:
		dbconn = sql.connect(sqlitedb)
		dbconn.text_factory = str
		cur = dbconn.cursor()
		sel = cur.execute("SELECT * FROM `users` WHERE `email` = ? ", (email,))
		finder = sel.fetchone()
		eCheck = validate_email(email)	#validates email, could do it myself but originally this library was supposed to send a message to the email server to check if the email is real
		if session.get('uid'):	#session already set
			final = "You are already logged in."
		elif finder:	#email already in db
			final = "An account with that email already exists."
		elif not eCheck:	#email form isn't an email
			final = "Invalid email."
		else:	#good to go
			hashedPass = bcrypt.hash(password1)	#hash bcrypt using secret key on top
			final = "registered"
			insertU = cur.execute("INSERT INTO `users` (email, pass) VALUES (?, ?)", (email, hashedPass))	#insert into DB
			dbconn.commit()

		dbconn.close()
	except:
			final = "Couldn't connect to the database. Please reload."
		
	return final
@app.route('/login', methods=['POST'])
def login():
	final = "Couldn't connect to the database. Please reload."
	email = request.form.get('email')	#email/pw post 
	password = request.form.get('pw')
	try:
		dbconn = sql.connect(sqlitedb)
		dbconn.text_factory = str
		cur = dbconn.cursor()
		sel = cur.execute("SELECT * FROM `users` WHERE `email` = (?) ", (email,))
		finder = sel.fetchone()
		if session.get('uid'):	#session already set
			final = "You are already logged in."
		elif not finder:	#email not found
			final = "Sorry, that E-mail doesn't exist."
		elif not bcrypt.verify(password, finder[2]):	#not correct password
			final = "Sorry, that is the wrong password."
		elif bcrypt.verify(password, finder[2]) and finder:	#probably doublelogic somewhere here but just in case, logged in
			final = "logged"
			session['uid'] = finder[0]	#set session
		else:
			final = "An unexpected error occured. Please try again."
		dbconn.close()
	except:
		final = "Couldn't connect to the database. Please reload."
		
	return final
	
@app.route('/logout')
def logout():
	final = ""
	session.pop('uid', None)	#pop that session out of here
	return final
@app.route('/add')
def add():
	return render_template('index.html', name='add')
	
@app.route('/edit')
def edit():
	return 0
@app.route('/take')
def take():
	return 0