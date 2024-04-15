from flask import Flask, request
import frontend_api

app = Flask(__name__)


@app.route("/analyze", methods=['POST'])
def analyze():
    print("Request received")
    data = request.get_json()
    print(data)
    result = frontend_api.frontend_api(data)
    return result


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"


@app.route("/get_current_status", methods=['GET'])
def get_current_status():
    return frontend_api.get_updates()


app.run(port=98, debug=True, host='0.0.0.0')
