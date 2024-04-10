from flask import Flask, request, jsonify
from frontend_api import frontend_api


app = Flask(__name__)


@app.route("/upload", methods=['POST'])
def upload():
    print("Request received")
    data = request.get_json()
    print(data)
    result = frontend_api(data)
    return result


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"


app.run(port=98, debug=True, host='0.0.0.0')



