
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json

import json
import argparse
import subprocess

parser = argparse.ArgumentParser()


questions = [
    {"type": "input",
     "name" : "first_name",
     "message" : "What is yo name"
     
     }
]

answers = prompt(questions)
print_json(answers)



"""
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--token", "-t", type=str, required=True)
args = parser.parse_args()
    
github_token = open(args.token,"r").read()

sbom_json = open(args.file)
sbom_data = json.load(sbom_json)
"""
github_repos = []

for value in sbom_data["components"]:
    dependency = value["name"]
    if "github.com" in dependency:
        github_repos.append(dependency)

print(github_token)
github_token_arg = f"GITHUB_AUTH_TOKEN={github_token}".strip("\n")

#openSSF_call = ["docker run", github_token_arg, "gcr.io/openssf/scorecard:stable", "--repo=github.com/ossf-tests/scorecard-check-branch-protection-e2e"]

test_call = f"sudo docker run -e {github_token_arg}  gcr.io/openssf/scorecard:stable --repo=github.com/ossf-tests/scorecard-check-branch-protection-e2e"
repo_score_dict = dict()

for dependency in github_repos:
    openSSF_call = f"sudo docker run -e {github_token_arg}  gcr.io/openssf/scorecard:stable --repo={dependency} --format json"
    print(f"Starting scorecard call on: {dependency} .....")
    call = subprocess.run(openSSF_call, shell=True, capture_output=True)
    print(f"done checking dependency: {dependency}")
    json_call = json.loads(call.stdout.decode("utf-8"))
    repo_score_dict[dependency] = json_call
    break


for key in repo_score_dict["github.com/0xAX/notificator"].keys():
    print(key)

    

