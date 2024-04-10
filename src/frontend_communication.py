from flask import Flask, request, jsonify

@app.route('/upload', methods=['POST'])
def upload():
	data = request.get_json()
	print("recieved data")
	return jsonify(data)

@app.route('/hello', methods=['GET'])
def hello():

	return "Hello World!"

