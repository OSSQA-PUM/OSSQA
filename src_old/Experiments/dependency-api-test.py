from typing import List, Tuple
import subprocess
import json
import requests
import os

def analyze_dependency_score(git_url: str) -> List[Tuple[str, int, str]]:
    """
    Analyzes the dependencies of a given Git repository using the OpenSSF Scorecard tool.
    
    Args:
        git_url (str): The URL of the Git repository to analyze.
        git_auth_token (str, optional): Authentication token for accessing private repositories. 
            Defaults to reading from a file if not provided.
    
    Returns:
        A list of tuples containing the name, score, and URL of each dependency check.
    """
    
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

    dependency_scores = []
    
    # Extract and store the score for each check performed by the Scorecard tool
    for check in json_output["checks"]:
        dependency_scores.append((check['name'], check['score'], git_url))
    
    return dependency_scores

def get_dependency_urls(SBOM) -> List[str]:
    """
    Extracts URLs of dependencies from a Software Bill of Materials (SBOM) file.
    
    Args:
        SBOM: The SBOM file in JSON format.
    
    Returns:
        A list of URLs of the dependencies.
    """
    data = json.load(SBOM)
    component_urls = []
    
    # Filter and collect URLs that start with 'github'
    for component in data["components"]:
        url = component["name"]
        if url.startswith("github"):
            component_urls.append(url)

    print(f"URLs extracted: {len(component_urls)} out of {len(data['components'])}")
    return component_urls

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

def calculate_avrage_token_use():
    """
    Calculates the average token usage by analyzing the dependency scores of component URLs.
    
    Returns:
    None
    """
    
    token_stats = check_token_usage()
    tokens_used = int(token_stats['used']) + 1
    first_tokens_used = tokens_used
    SBOM = open('C:\Programming\Kandidat\OSSQA\src\Experiments\example-SBOM.json')
    component_urls = get_dependency_urls(SBOM)
    
    costs = []

    for i in range(len(component_urls)):
        print(f"Analyzing {i+1}/{len(component_urls)}: {component_urls[i]}")
        last_token_stats = token_stats
        analyze_dependency_score(component_urls[i])
        token_stats = check_token_usage()
        tokens_used = int(token_stats['used']) + 1
        costs.append(int(token_stats['used']) - int(last_token_stats['used']))
    
    print(costs)
    
    token_stats = check_token_usage()
    print("Total tokens used:", int(token_stats['used']) - first_tokens_used - len(component_urls))


if __name__ == "__main__":
    calculate_avrage_token_use()