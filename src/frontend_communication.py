from flask import Flask, request
import mas
from util import UserRequirements
from job_observer import JobModelSingleton, JobListerner


def parse_user_reqs(user_reqs: str) -> UserRequirements:
    """
    Parses the user requirements from the request headers.

    Args:
        user_reqs (str): The user requirements.

    Returns:
        list[int]: The user requirements as a list of integers.
    """
    if not user_reqs:
        print("No user reqs, using default values [10,10,10,10,10]")
        return UserRequirements()
    reqs_list: list[int] = user_reqs.strip(" ").strip("[").strip("]").split(",")

    try:
        for i, req in enumerate(reqs_list):
            reqs_list[i] = int(req)
            assert 0 <= reqs_list[i] <= 10
    except (AssertionError, ValueError):
        print("Invalid reqs, using default values [10,10,10,10,10]")
        reqs_list = [10, 10, 10, 10, 10]

    user_reqs: UserRequirements = UserRequirements(
        reqs_list[0], reqs_list[1], reqs_list[2],
        reqs_list[3], reqs_list[4]
    )

    return user_reqs


app = Flask(__name__)

listener = JobListerner()
job_model = JobModelSingleton()
job_model.register_observer(listener)

@app.errorhandler(415)
def page_not_found(error):
    print("Error:", error)
    return "Not found", 415


@app.route("/analyze", methods=['POST'])
def analyze():
    print("Request received")
    try:
        user_reqs_param = request.headers.get('user_reqs')
    except KeyError:
        user_reqs_param = "[10,10,10,10,10]"
    
    print("User reqs:", user_reqs_param)
    user_reqs: UserRequirements = parse_user_reqs(user_reqs_param)
    data = request.get_json()
    print(data)
    result = mas.validate_input(str(data), user_reqs)
    return result


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"


@app.route("/get_current_status", methods=['GET'])
def get_current_status():
    return job_model.__dict__()


app.run(port=98, debug=True, host='0.0.0.0')
