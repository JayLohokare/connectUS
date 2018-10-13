from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/register', methods=['GET'])
def get_tasks():
	args = request.args
	phone = args['phone']
	return phone

if __name__ == '__main__':
    app.run(debug=True)