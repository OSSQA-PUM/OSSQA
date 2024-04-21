import requests
import json
from data_types.sbom_types.scorecard import Scorecard

def test():
    res = requests.get("https://api.securityscorecards.dev/projects/github.com/jonschlinkert/pad-left")
    with open("main/tests/unit_tests/scorecards/pad-left.json", "w", encoding="utf-8") as f:
        res_json = json.dumps(res.json(), indent=4)
        f.write(res_json)