import json
from dataclasses import asdict

from flask import Flask, request
from main.frontend.front_end_api import FrontEndAPI
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import (UserRequirements,
                                               RequirementsType)
from main.sbom_processor import SbomProcessorStatus
import requests
import main.constants as constants

app = Flask(__name__)
frontend_api = FrontEndAPI(constants.HOST)
status: SbomProcessorStatus = SbomProcessorStatus("Initializing")


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
    except (KeyError, TypeError):
        user_reqs_param = "[10, 10, 10, 10, 10,10, 10, 10, 10, 10,10, 10, 10, 10, 10, 10, 10, 10]"
    user_reqs_param = json.loads(user_reqs_param)
    user_reqs_dict = {
        RequirementsType.VULNERABILITIES: user_reqs_param["Vulnerabilities"],
        RequirementsType.DEPENDENCY_UPDATE_TOOL: user_reqs_param["Dependency Update Tool"],
        RequirementsType.MAINTAINED: user_reqs_param["Maintained"],
        RequirementsType.SECURITY_POLICY: user_reqs_param["Security Policy"],
        RequirementsType.LICENSE: user_reqs_param["License"],
        RequirementsType.CII_BEST_PRACTICES: user_reqs_param["CII Best Practices"],
        RequirementsType.CI_TESTS: user_reqs_param["CI Tests"],
        RequirementsType.FUZZING: user_reqs_param["Fuzzing"],
        RequirementsType.SAST: user_reqs_param["SAST"],
        RequirementsType.BINARY_ARTIFACTS: user_reqs_param["Binary Artifacts"],
        RequirementsType.BRANCH_PROTECTION: user_reqs_param["Branch Protection"],
        RequirementsType.DANGEROUS_WORKFLOW: user_reqs_param["Dangerous Workflow"],
        RequirementsType.CODE_REVIEW: user_reqs_param["Code Review"],
        RequirementsType.CONTRIBUTORS: user_reqs_param["Contributors"],
        RequirementsType.PINNED_DEPENDENCIES: user_reqs_param["Pinned Dependencies"],
        RequirementsType.TOKEN_PERMISSIONS: user_reqs_param["Token Permissions"],
        RequirementsType.PACKAGING: user_reqs_param["Packaging"],
        RequirementsType.SIGNED_RELEASES: user_reqs_param["Signed Releases"]
        }

    try:
        user_reqs: UserRequirements = UserRequirements(user_reqs_dict)
    except (AssertionError, ValueError):
        return "Invalid user requirements", 415

    try:
        sbom = Sbom(json.loads(data['sbom']))
    except (KeyError, TypeError):
        return "Invalid SBOM", 415
    frontend_api.subscribe_to_state_change(update_current_status)
    result_sbom: Sbom = frontend_api.analyze_sbom(sbom, user_reqs)

    result_json = result_sbom.to_dict_web()
    return json.dumps(result_json)


@app.route("/hello", methods=['GET'])
def hello():
    """test function"""
    return "Hello World!"


def update_current_status(update: SbomProcessorStatus):
    """
    Updates the current status of the request.
    """
    global status
    status = update


@app.route("/get_current_status", methods=['GET'])
def get_current_status():
    global status
    print(f"Status updated: {asdict(status)}")
    return json.dumps(asdict(status))


@app.route("/get_previous_sbom/<path:repo_name>", methods=['GET'])
def get_previous_sboms(repo_name: str):
    print(f"Looking up previous SBOMs for {repo_name}")
    sboms = frontend_api.lookup_previous_sboms(repo_name)
    sbom_dicts = [sbom.to_dict() for sbom in sboms]
    return json.dumps(sbom_dicts)


def run():
    app.run(port=98, debug=True, host='0.0.0.0')
