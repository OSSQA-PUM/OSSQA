from flask import Flask, request
import json
import front_end_api
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import UserRequirements

app = Flask(__name__)
frontend_api = front_end_api.FrontEndAPI()
status: str = "Idle"


@app.errorhandler(415)
def page_not_found(error):
    print("Error:", error)
    return "Not found", 415


@app.route("/analyze", methods=['POST'])
def analyze():
    """
    Analyzes an SBOM.
    Returns:
        str: The analyzed SBOM.
    """
    print("Request received")
    data = request.get_json()
    try:
        user_reqs_param = data['user_reqs']
    except KeyError:
        user_reqs_param = "[10,10,10,10,10]"
    user_reqs: UserRequirements = UserRequirements(user_reqs_param)
    print(user_reqs.to_dict())
    sbom = Sbom.from_dict(data['sbom'])
    print("\n\n\n")
    print(sbom.to_dict())
    frontend_api.subscribe_to_state_change(lambda x: update_current_status(x))
    result_sbom: Sbom = frontend_api.analyze_sbom(sbom, user_reqs)
    result_json = result_sbom.to_dict()
    return json.dumps(result_json)


@app.route("/hello", methods=['GET'])
def hello():
    """test function"""
    return "Hello World!"


def update_current_status(update: str):
    """
    Updates the current status of the request.
    """
    global status
    status = update


@app.route("/get_current_status", methods=['GET'])
def get_current_status():
    return status


app.run(port=98, debug=True, host='0.0.0.0')
