from __future__ import print_function # In python 2.7

from twilio import twiml
import flask

from twilio.rest import Client

from flask import Flask, jsonify
from flask import request, redirect

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather

import sys
import string
import random
import logging
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import difflib
import csv
import requests
				
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


app = Flask(__name__)

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred, {
   "databaseURL": "https://globalhacks7.firebaseio.com",
})


# 127.0.0.1:5000/register?phone=1234&name=Jay&location=saintLouis&nationality=Indian&messengerType=Whatsapp&groupName=Trial
@app.route('/registerPatron', methods=['GET'])
def register_patron():
	args = request.args
	phone = args['phone']
	location = args['location']
	nationality = args['nationality']
	messengerType = args['messengerType']
	groupName = args['groupName']
	name = args['name']

	data = {"name":name, "phone": phone, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	
	root = db.reference()
	ref  = root.child('patron')	
	userRef = ref.push(data)
	return "Success"


@app.route('/registerImmigrant', methods=['GET'])
def register_immigrant():
	args = request.args
	phone = args['phone']
	name = args['name']
	patronPhone = args['patronPhone']

	val = list(db.reference('patron').order_by_child("phone").equal_to(patronPhone).get().values())[0]
	location = val['location']
	nationality = val['nationality']
	groupName = val['groupName']
	messengerType = val['messengerType']
	
	data = {"name":name, "phone": phone, "location": location, "patronPhone": patronPhone, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	
	root = db.reference()
	ref  = root.child('immigrants')	
	userRef = ref.push(data)
	return "Success"


#127.0.0.1:5000/postEvent?event=LOLOLOL&patronPhone=12345&messengerType=FB
@app.route('/postEvent', methods=['GET'])
def post_events():
	args = request.args
	eventData = args['event']
	messengerType = args['messengerType']
	patronNumber = str(args['patronPhone'])

	val = list(db.reference('patron').order_by_child("phone").equal_to(patronNumber).get().values())[0]
	location = val['location']
	nationality = val['nationality']
	groupName = val['groupName']
	data = {"event":eventData, "patronPhone": patronNumber, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	root = db.reference()
	new_user = root.child('events').push(data)
	return "Success"

#http://127.0.0.1:5000/getEvent?location=NYC
@app.route('/getEvent', methods=['GET'])
def get_events():
	args = request.args
	if "location" in args:
		val = list(db.reference('events').order_by_child("location").equal_to(args['location']).get().values())
	else:
		val = list(db.reference('events').get().values())
	
	return str(val)

			
@app.route('/postQuery', methods=['POST'])
def post_query():

	thisNationality = "Mexican" #Hardcoded as a number corresponds to only one language

	try:
		if request.values.get('sound'):
			sound = request.values.get('sound')
			body = request.values.get('Body')
			sender = request.values.get('From')

			enc = ""
			for i in sender[1:]:
				enc += (i)
				enc+= random.choice(string.ascii_letters)
			message =   "Someone needs your help \nHere is the question: \n" + body + "\nYou have received an audio file" + "\n" + sound + "\n" + "https://wa.me/14155238886?text=ID" + enc + "\n\n"

			val = list(db.reference('patron').order_by_child("nationality").equal_to(thisNationality).get().values())[0]
			for i in val:
				phNo = i['phone']
				requests.get("http://127.0.0.1:5000/sendWhatsAppMessage?to=" + phNo + "&message=" + message )
		

			return "SUCCESS"
		
	except:
		pass

	print (body.values)
	body = request.values.get('Body', None).lower()
	
	phoneNumber = request.values.get('From')
	
	receiver = ""
	
	if body[0:2].lower() == "id":
		receiver = ""
		i = 2
		while i < 22:
			receiver += body[i]
			i += 2
		
		requests.get("http://127.0.0.1:5000/sendWhatsAppMessage?to=" + receiver + "&message=" + body[24:])
		return "Success"
	#whatsapp://send?text=Hello World!&phone=+9198********1

	args = request.args
	
	textBody = ""

	region = ""
	#Region extraction
	placesDict = {"saint louis", "new york", "san diego", "las vegas", "los angeles", "san francisco"}
	for i in placesDict:
		if i in body:
			region = i

	foundFAQ = False
	with open('FAQs.csv', encoding="utf8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			question = str(row[0])
			if question == body:
				foundFAQ = True
				requests.get("http://127.0.0.1:5000/sendWhatsAppMessage?to=" + phoneNumber + "&message=" + str(row[1]) )
				break
				
		if not foundFAQ:
			#Send question to the a patrons in area
			# deepLink = "https://wa.me/14155238886&text="+phoneNumber[1:]
			enc = ""
			for i in phoneNumber[10:]:
				enc += (i)
				enc+= random.choice(string.ascii_letters)
			message =   "Someone needs your help \nHere is the question: \n" + body + "\n" + "https://wa.me/14155238886?text=ID" + enc + "\n\n"

			val = list(db.reference('patron').order_by_child("nationality").equal_to(thisNationality).get().values())[0]
			for i in val:
				phNo = i['phone']
				requests.get("http://127.0.0.1:5000/sendWhatsAppMessage?to=" + phNo + "&message=" + message )
				
			
	data = {"phone":phoneNumber, "nationality": nationality, "query": textBody, "region":region}
	root = db.reference()
	new_user = root.child('queries').push(data)

	return "Success"




@app.route('/sendWhatsAppMessage', methods=['GET'])
def send_WP_message():
	args = request.args
	to = args['to']
	message = args['message']
		
	from twilio.rest import Client

	account_sid = 'ACe58e52bde56b9659bb7dfe80653d31b6'
	auth_token = '4572801f338e4e4f94d4772985e130ec'
	client = Client(account_sid, auth_token)

	message = client.messages.create(
					body=message,
					from_='whatsapp:+14155238886',
					to='whatsapp:+16319979047'
				)

	print(message.sid)

	return "Success"

@app.route('/getQuery', methods=['GET'])
def get_queries():
	args = request.args
	if "location" in args:
		val = list(db.reference('queries').order_by_child("location").equal_to(args['location']).get().values())
	else:
		val = list(db.reference('queries').get().values())
	
	return str(val)



@app.route('/getWhatsAppMessage', methods=['POST'])
#Broadcast here
def handle_get_WP_message():
	body = request.values.get('Body', None)

	from TwitterAPI import TwitterAPI
  
	# personal details 
	consumer_key ="5YGcUrIGaEk9HMo9niSiv3elv"
	consumer_secret ="3QPKtpIUtWb2m1NWmjhKi4szhCporKOEC84sEJer9Oo8VHazx3"
	access_token ="2405586890-Gj5ThOKtDIedJneZhXeNpV2WL8S5zLxgBk17O69"
	access_token_secret ="f2wBmpZ23mFahiK3P7sjgONPFqSymawL7ZU8Yxh8fyFEG"
	
	api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret)

	r = api.request('statuses/update', {'status': body})
	print ('SUCCESS' if r.status_code == 200 else 'FAILURE')

	resp = MessagingResponse()
	resp.message(body)

	#body

	return str(resp)


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp


@app.route("/handleVoiceResponse", methods=['GET', 'POST'])
def handleVoiceREsponse():
	soundURL = (request.values['RecordingUrl'])
	print (request.values)
	data = {'sound': soundURL, "From": request.values['From'], "Body": request.values['TranscriptionText']} 

	return 'Success'


@app.route("/handleVoice", methods=['GET', 'POST'])
def handleVoice():
	resp = VoiceResponse()

	if 'Digits' in request.values:
		# Get which digit the caller chose
		choice = request.values['Digits']

		phone = request.values['From']


		# <Say> a different message depending on the caller's choice
		if choice == '1':
			
			resp2 = VoiceResponse()
			resp2.say("Hi, how can I help you today?", voice='alice', language="en-US")

			resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
			print(resp2)
			return str(resp2)

		elif choice == '2':
			resp2 = VoiceResponse()
			resp2.say("Hola como puedo ayudarte hoy?", voice='alice', language="es-MX")
			
			resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
			print(resp2)
			return str(resp2)

		elif choice == '3':
			resp2 = VoiceResponse()
			resp2.say("嗨，我今天怎么能帮到你？", voice='alice', language="zh-CN")
			
			resp2.record(timeout=5, transcribe=True, transcribeCallback="/handleVoiceResponse")
			print(resp2)
			return str(resp2)

		else:
			resp.say("Sorry, I dint understand the input")
			return ""
		


	return ""

	

@app.route("/voice", methods=['GET', 'POST'])
def voice():
	resp = VoiceResponse()
	# Start our <Gather> verb
	g = Gather(num_digits=1, action='/handleVoice')
	g.say("Welcome, press one for English", voice='alice', language="en-US")
	g.say("Bienvenido, para español, presione 2", voice='alice', language="es-MX")
	g.say("欢迎，按3为中文", voice='alice', language="zh-CN")
	resp.append(g)

	# If the user doesn't select an option, redirect them into a loop
	resp.redirect('/voice')

	return str(resp)

	
    
if __name__ == '__main__':
    app.run(debug=True)


