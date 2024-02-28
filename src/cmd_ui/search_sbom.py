
from __future__ import print_function, unicode_literals
import glob
import json
import os
import argparse
import subprocess
from subprocess import call
parser = argparse.ArgumentParser()

def get_choice():
    choice = input(": ")
    return choice.strip()


def display_ui():
    print("What would you like to do?")
    print("1. Search SBOM")
    print("2. Edit token")
    print("3. Exit")


def display_tokens():
    print("Choose a token:")
    files = search_files()
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files


def edit_token():
    files = display_tokens()
    user_choice = int(get_choice()) - 1
    if 0 <= user_choice < len(files):
        return files[user_choice]
    else:
        print("Invalid choice.")
        return None


def main():
    while True:
        display_ui()
        user_choice = get_choice()

        if user_choice == "1":
            print("tjo")

        elif user_choice == "2":
            # TODO: kanske dra ut detta till en separat funktion? 
            os.system('cls' if os.name == 'nt' else 'clear')
            chosen_file = edit_token()
            if chosen_file is not None:
                token = open(chosen_file, "r").read()
                print(f"New token: {token}")

        elif user_choice == "3":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose again.")



def search_files():
    # TODO: denna hittar bara requirements.txt, hann inte kolla på det
    files = [f for f in glob.glob("*.txt")]
    print(files)
    return files



"""
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--token", "-t", type=str, required=True)
args = parser.parse_args()
    
github_token = open(args.token,"r").read()

sbom_json = open(args.file)
sbom_data = json.load(sbom_json)
"""
""" github_repos = []

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

 """    

if __name__ == "__main__":
    main()