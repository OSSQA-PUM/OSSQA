
from dataclasses import dataclass
import os
import requests

@dataclass
class Dependency:
    """
    Represents a dependency for a project.

    Attributes:
        json_component (dict): The JSON representation of the dependency.
        platform (str): The platform on which the dependency is used.
        repo_owner (str): The owner of the repository 
                          where the dependency is hosted.
        repo_name (str): The name of the repository 
                         where the dependency is hosted.
        url (str): The URL of the dependency.
        failure_reason (Exception): The reason for any failure 
                                    related to the dependency.
        dependency_score (dict): The scorecard related to the dependency.
    """
    json_component: dict = None
    platform: str = None
    repo_owner: str = None
    repo_name: str = None
    url: str = None
    failure_reason: Exception = None
    dependency_score: dict = None

def check_token_usage():
    """
    Check the usage of the GitHub Personal Access Token.

    Returns:
        dict: A dictionary containing the token usage information, including the limit, used, and remaining counts.
              Returns None if the authentication fails.
    """
    
    # Replace 'your_token_here' with your actual GitHub Personal Access Token
    token = os.environ.get('GITHUB_AUTH_TOKEN')

    # The GitHub API URL for the authenticated user
    url = 'https://api.github.com/user'

    # Make a GET request to the GitHub API with your token for authentication
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers, timeout=5)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.headers
    
        return {"limit": user_data['X-RateLimit-Limit'], "used": user_data['x-ratelimit-used'], "remaining": user_data['X-RateLimit-Remaining']}

    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        return None
    
if __name__ == "__main__":
    print(check_token_usage())