import json
from flask import Flask, request
from main.frontend.front_end_api import FrontEndAPI
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import (UserRequirements,
                                               RequirementsType)
from main.sbom_processor import SbomProcessorStatus

app = Flask(__name__)
frontend_api = FrontEndAPI()
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
        user_reqs_param = "[10, 10, 10, 10, 10]"
    user_reqs_param = json.loads(user_reqs_param)
    user_reqs_dict = {
        RequirementsType.CODE_VULNERABILITIES: user_reqs_param[0],
        RequirementsType.MAINTENANCE: user_reqs_param[1],
        RequirementsType.CONTINUOUS_TESTING: user_reqs_param[2],
        RequirementsType.SOURCE_RISK_ASSESSMENT: user_reqs_param[3],
        RequirementsType.BUILD_RISK_ASSESSMENT: user_reqs_param[4]
        }
    
    try:
        user_reqs: UserRequirements = UserRequirements(user_reqs_dict)
    except (AssertionError, ValueError):
        return "Invalid user requirements", 415
    
    sbom = Sbom(json.loads(data['sbom']))
    print("\n\n\n")
    print(sbom.to_dict())
    frontend_api.subscribe_to_state_change(update_current_status)
    result_sbom: Sbom = frontend_api.analyze_sbom(sbom, user_reqs)
    result_json = result_sbom.to_dict()
    return json.dumps(result_json)


@app.route("/hello", methods=['GET'])
def hello():
    """test function"""
    return "Hello World!"


def update_current_status(update: SbomProcessorStatus):
    """
    Updates the current status of the request.
    """
    print(f"Status updated: {update}")


@app.route("/get_current_status", methods=['GET'])
def get_current_status():
    return status


def run():
    app.run(port=98, debug=True, host='0.0.0.0')
