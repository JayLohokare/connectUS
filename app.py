from __future__ import print_function # In python 2.7
from flask import Flask, jsonify
from flask import request
import sys
import logging
import sys

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials

from firebase_admin import db

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred, {
   "databaseURL": "https://globalhacks7.firebaseio.com",
})

# 127.0.0.1:5000/register?phone=1234&name=Jay&location=saintLouis&nationality=Indian&messengerType=Whatsapp&groupName=Trial

root = db.reference()
ref  = root.child('patron')	
	

@app.route('/register', methods=['GET'])
def get_tasks():
	args = request.args
	phone = args['phone']
	location = args['location']
	nationality = args['nationality']
	messengerType = args['messengerType']
	groupName = args['groupName']
	name = args['name']

	data = {"name":name, "phone": phone, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}

	userRef = ref.push(data)
	
	return phone


@app.route('/postEvent', methods=['GET'])
def post_events():
	args = request.args
	eventData = args['event']
	patronNumber = str(args['patronPhone'])

	val = list(db.reference('patron').order_by_child("phone").equal_to(patronNumber).get().values())[0]
	
	location = val['location']
	nationality = val['nationality']
	messengerType = "Whatsapp"#This comes via Twilio""
	groupName = val['groupName']
	
	data = {"event":eventData, "patronPhone": patronNumber, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}

	root = db.reference()
	new_user = root.child('events').push(data)

	return "Success"

			

if __name__ == '__main__':
    app.run(debug=True)