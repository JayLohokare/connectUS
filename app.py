from __future__ import print_function # In python 2.7
from flask import Flask, jsonify
from flask import request
import sys
import logging
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


app = Flask(__name__)

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred, {
   "databaseURL": "https://globalhacks7.firebaseio.com",
})


	
# 127.0.0.1:5000/register?phone=1234&name=Jay&location=saintLouis&nationality=Indian&messengerType=Whatsapp&groupName=Trial
@app.route('/register', methods=['GET'])
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

			
@app.route('/postQuery', methods=['GET'])
def post_query():
	args = request.args
	phoneNumber = args['phone']
	nationality = args['nationality']
	messenger = args['messenger']
	query = args['query']
	
	data = {"phone":phoneNumber, "nationality": nationality, "messenger": messenger, "query": query}
	root = db.reference()
	new_user = root.child('queries').push(data)

	return "Success"

@app.route('/getQuery', methods=['GET'])
def get_queries():
	args = request.args
	if "location" in args:
		val = list(db.reference('queries').order_by_child("location").equal_to(args['location']).get().values())
	else:
		val = list(db.reference('queries').get().values())
	
	return str(val)

if __name__ == '__main__':
    app.run(debug=True)