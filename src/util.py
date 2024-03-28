"""
This module contains utility functions and classes for the project.

Functions:
    check_token_usage: Check the usage of the GitHub Personal Access Token.
    contains_all_checks: Check if the scorecard contains the required checks.
    validate_scorecard: Validate the scorecard.

Classes:
    Checks: Represents the checks that can be performed on a dependency.
    UserRequirements: Represents the user requirements for a project.
    Dependency: Represents a dependency for a project.
"""
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
class UserRequirements:
    """
    Represents the user requirements for a project.

    Attributes:
        source_risk_assessment (int): The risk assessment of the source.
        maintence (int): The maintenance of the project.
        build_risk_assessment (int): The risk assessment of the build.
        continuous_testing (int): The continuous testing of the project.
        code_vunerabilities (int): The code vulnerabilities of the project.
    """
    source_risk_assessment: int = 10
    maintence: int = 10
    build_risk_assessment: int = 10
    continuous_testing: int = 10
    code_vunerabilities: int = 10

    def validate(self):
        """
        Validate the user requirements.

        Raises:
            ValueError: If the user requirements are invalid.
        """
        if not (isinstance(self.source_risk_assessment, int) and
                isinstance(self.maintence, int) and
                isinstance(self.build_risk_assessment, int) and
                isinstance(self.continuous_testing, int) and
                isinstance(self.code_vunerabilities, int)):
            raise TypeError("input arguments are not integers")

        if not (0 <= self.source_risk_assessment <= 10 and
                0 <= self.maintence <=10 and
                0 <= self.build_risk_assessment <= 10 and
                0 <= self.continuous_testing <= 10 and
                0 <= self.code_vunerabilities <= 10):
            raise ValueError(
                "input arguments fall out of bounds,\
                check if input variables are within the bounds 0 to 10")


@dataclass
class Dependency:
    """
    Represents a dependency for a project.

    Attributes:
        json_component (dict): The JSON representation of the dependency.
        platform (str): The platform on which the dependency is used.
        repo_path (str): The path to the repo
        url (str): The URL of the dependency.
        failure_reason (Exception): The reason for any failure 
                                    related to the dependency.
        dependency_score (dict): The scorecard related to the dependency.
    """
    json_component: dict = None
    platform: str = None
    repo_path: str = None
    url: str = None
    failure_reason: Exception = None
    dependency_score: dict = None

    def __eq__(self, other):
        """
        Check if two dependencies are equal.

        Args:
            other (Dependency): The other dependency to compare with.

        Returns:
            bool: True if the dependencies are equal, False otherwise.
        """
        name_version = self.platform + self.repo_owner + self.repo_name
        other_name_version = other.platform + other.repo_owner + other.repo_name
        return name_version == other_name_version

    def to_dict(self) -> dict:
        """
        Convert the dependency to a dictionary.

        Returns:
            dict: The dictionary representation of the dependency.
        """
        return {
            "platform": self.platform,
            "repo_owner": self.repo_owner,
            "repo_name": self.repo_name,
            "url": self.url,
            "dependency_score": self.dependency_score
        }



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

        return {
            "limit": user_data['X-RateLimit-Limit'],
            "used": user_data['x-ratelimit-used'],
            "remaining": user_data['X-RateLimit-Remaining']
            }

    print(f"Failed to authenticate. Status code: {response.status_code}")
    return None


def contains_all_checks(scorecard_checks: list[dict]) -> bool:
    """
    Check if the scorecard contains the required checks.

    Args:
        scorecard_checks (dict): The scorecard to be checked.

    Returns:
        bool: True if the scorecard contains the required checks, 
        False otherwise.
    """
    not_found = [] + Checks.all()

    for check in scorecard_checks:
        check_name = check["name"]

        if "score" not in check:
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
