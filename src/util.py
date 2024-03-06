
from dataclasses import dataclass
from enum import StrEnum
import os
import requests

class Checks(StrEnum):
    """
    Represents the checks that can be performed on a dependency.
    """
    BINARY_ARTIFACTS = "Binary-Artifacts"
    BRANCH_PROTECTION = "Branch-Protection"
    CI_TESTS = "CI-Tests"
    CII_BEST_PRACTICES = "CII-Best-Practices"
    CODE_REVIEW = "Code-Review"
    CONTRIBUTORS = "Contributors"
    DANGEROUS_WORKFLOW = "Dangerous-Workflow"
    DEPENDENCY_UPDATE_TOOL = "Dependency-Update-Tool"
    FUZZING = "Fuzzing"
    LICENSE = "License"
    MAINTAINED = "Maintained"
    PACKAGING = "Packaging"
    PINNED_DEPENDENCIES = "Pinned-Dependencies"
    SAST = "SAST"
    SECURITY_POLICY = "Security-Policy"
    SIGNED_RELEASES = "Signed-Releases"
    TOKEN_PERMISSIONS = "Token-Permissions"
    VULNERABILITIES ="Vulnerabilities"

    @classmethod
    def all(cls):
        """
        Get all checks.

        Returns:
            list: A list of all checks.
        """
        return list(Checks)


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

    def get_check(self, name: Checks) -> dict:
        """
        Get the check with the given name from the dependency scores.

        Args:
            name (str): The name of the check.
        
        Returns:
            dict: The check with the given name.
        """
        for check in self.dependency_score["checks"]:
            if check["name"] == name:
                return check
        return None

def check_token_usage():
    """
    Check the usage of the GitHub Personal Access Token.

    Returns:
        dict: A dictionary containing the token usage information, 
              including the limit, used, and remaining counts.
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


def contains_all_checks(scorecard_checks: list[dict]) -> bool:
    """
    Check if the scorecard contains the required checks.

    Args:
        scorecard (dict): The scorecard to be checked.

    Returns:
        bool: True if the scorecard contains the required checks, 
        False otherwise.
    """
    not_found = [] + Checks.all()

    for check in scorecard_checks:
        check_name = check["name"]

        if "score" not in check:
            return False
        if not check["score"]:
            return False
        if check_name in not_found:
            not_found.remove(check_name)
    return not not_found


def validate_scorecard(scorecard: dict) -> bool:
    """
    Validate the scorecard.

    Args:
        scorecard (dict): The scorecard to be validated.

    Returns:
        bool: True if the scorecard is valid, False otherwise.
    """
    try:
        scorecard_checks:list[dict] = scorecard["checks"]
    except KeyError:
        return False

    return contains_all_checks(scorecard_checks)


if __name__ == "__main__":
    print(check_token_usage())
