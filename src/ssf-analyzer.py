import requests
import os
import subprocess
import json

# get git sha1 number
def get_git_sha1_number(repo_owner, repo_name) -> str:
    """
    Gets the SHA-1 hash of the latest commit of a Git repository.
    
    Args:
        git_url (str): The URL of the Git repository.
    
    Returns:
        The SHA-1 hash of the latest commit.
    """
    # Call the GitHub API
    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits")
    
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()[0]["sha"]
    else:
        return None

def check_token_usage():
    # Replace 'your_token_here' with your actual GitHub Personal Access Token
    token = os.environ.get('GITHUB_AUTH_TOKEN')

    # The GitHub API URL for the authenticated user
    url = 'https://api.github.com/user'

    # Make a GET request to the GitHub API with your token for authentication
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.headers
    
        return {"limit": user_data['X-RateLimit-Limit'], "used": user_data['x-ratelimit-used'], "remaining": user_data['X-RateLimit-Remaining']}

    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        return None

def try_get_from_ssf_api(platform, repo_owner, repo_name, commit_sha1 = None):
    """
    Tries to get the Software Bill of Materials (SBOM) from the Software Supply Chain (SSF) API.
    
    Args:
        commit_sha1 (str): The commit SHA-1 hash.
        platform (str): The platform name.
        repo_owner (str): The repository owner.
        repo_name (str): The repository name.
    
    Returns:
        The SBOM file in JSON format, or None if not found.
    """
    # Call the SSF API
    response = requests.get(f"https://api.securityscorecards.dev/projects/{platform}/{repo_owner}/{repo_name}" + (f"?commit={commit_sha1}" if commit_sha1 else ""))
    
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_scorecard_score(git_url: str):
    # Execute the Scorecard tool in a Docker container, passing the necessary environment variables
    output = subprocess.check_output(
        f'scorecard --repo={git_url} --show-details --format json', 
        shell=True
    )
    
    # Decode and clean the output for JSON parsing
    output = output.decode("utf-8")
    output = output.replace("failed to get console mode for stdout: The handle is invalid.", "")
    output = output.replace("\n", "")

    json_output = json.loads(output) 

    return json_output

def get_scorecard_score(platform, repo_owner, repo_name, git_url):
    sha1 = get_git_sha1_number(repo_owner=repo_owner, repo_name=repo_name)
    scorecard_score = try_get_from_ssf_api(platform=platform, repo_owner=repo_owner, repo_name=repo_name, commit_sha1=sha1)
    if scorecard_score is None:
        scorecard_score = analyze_scorecard_score(git_url)
    
    return scorecard_score

if __name__ == "__main__":
    url = "https://github.com/ossf/scorecard/tree/v4.13.1"
    url_split = url.replace("https://", "").split("/")
    platform = url_split[0]

    if platform == "github.com":
        repo_owner = url_split[1]
        repo_name = url_split[2]
    else:
        raise Exception("Platform not supported")

    #print(get_git_sha1_number(repo_owner=repo_owner, repo_name=repo_name))

    scorecard_score = get_scorecard_score(platform=platform, repo_owner=repo_owner, repo_name=repo_name, git_url=url)
    print(scorecard_score)