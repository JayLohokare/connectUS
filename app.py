from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred, {
   "databaseURL": "https://globalhacks7.firebaseio.com",
})

# 127.0.0.1:5000/register?phone=1234&name=Jay&location=saintLouis&nationality=Indian&messengerType=Whatsapp&groupName=Trial

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
	
	from firebase_admin import db
	root = db.reference()
	new_user = root.child('patron').push(data)
	
	return phone

if __name__ == '__main__':
    app.run(debug=True)