"""
This module contains utility functions for the main module.

Functions:
- get_git_sha1: Gets the SHA1 hash for a version of a dependency.
- is_valid_sha1: Check the validity of a sha1 string.
"""
import re
import os
import datetime
from math import inf
from time import time
import requests


class TokenLimitExceededError(Exception):
    """
    Exception raised when the GitHub API rate limit is exceeded.
    """
    reset_time: int
    message: str

    @property
    def reset_datetime(self) -> str:
        """
        Returns:
            str: The date and time at which the rate limit will be reset.
        """
        reset_datetime = datetime.datetime.fromtimestamp(int(self.reset_time))
        reset_datetime = reset_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return reset_datetime

    @property
    def time_to_wait(self) -> float:
        """
        Returns:
            float: The time in seconds remaining until the rate limit is reset.
        """
        return self.reset_time - time()

    def __init__(self, reset_time: str):
        """
        Initializes the TokenLimitExceededError.

        Args:
            reset_time (str): The time at which the rate limit will be reset.

        Raises:
            ValueError: If the reset time is not a valid integer.
        """
        self.reset_time = int(reset_time)
        self.message = (f"GitHub API rate limit exceeded. Try again later. "
                         f"Rate limit resets at {reset_time}.")
        super().__init__(reset_time)

    def __str__(self) -> str:
        return self.message


class Sha1NotFoundError(Exception):
    """
    Exception raised when the SHA1 hash for a version of a dependency is not
    found.
    """

    message: str

    def __init__(self, message: str = "SHA1 hash not found."):
        super().__init__(message)


def get_token_data() -> dict:
    """
    Returns:
        dict: A dictionary containing the user's GitHub API token data

    Raises:
        requests.ConnectionError: If the request to the GitHub API is
        unsuccessful.
    """
    token = get_github_token()
    url = 'https://api.github.com/rate_limit'

    # Make a GET request to the GitHub API with your token for authentication
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers, timeout=5)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.headers

        return {
            "limit": int(user_data['X-RateLimit-Limit']),
            "used": int(user_data['x-ratelimit-used']),
            "remaining": int(user_data['X-RateLimit-Remaining']),
            "reset_time": int(user_data["X-RateLimit-Reset"])
        }

    raise requests.ConnectionError(
        f"Failed to authenticate token. Status code: {response.status_code}"
        )


def get_git_sha1(git_url: str, version: str) -> str:
    """
    Get the SHA1 hash for a version of a dependency.

    Args:
        git_url (str): The URL of the GitHub repository.
        version (str): The version of the dependency.

    Returns:
        str: The SHA1 hash of the dependency version.

    Raises:
        ValueError: If the GitHub authentication token is not found in the
        environment.

        ConnectionRefusedError: If the request to the GitHub API is
        unsuccessful.

        TokenLimitExceededError: If the GitHub API rate limit is exceeded.

        AssertionError: If the found SHA1 hash is not valid.

        Sha1NotFoundError: If the SHA1 hash for the dependency version is not
        found.
    """

    # Get the GitHub authentication token
    token = get_github_token()
    headers = {'Authorization': f'token {token}'} if token else {}

    # Check that the release version exists
    url = f"https://api.github.com/repos/{git_url}/git/matching-refs/tags"
    response = requests.get(url, headers=headers, timeout=10)

    # Check if token is depleted
    if response.status_code == 403:
        token_data = get_token_data()
        raise TokenLimitExceededError(token_data["reset_time"])

    # Check if the request was successful
    if response.status_code != 200:
        raise ConnectionRefusedError(
            f"Failed to get tags. Status code: {response.status_code}"
            )

    # Filter out unwanted characters from the version
    original_version = version
    version.strip("-").strip("v").strip("@40")

    # Get the SHA1 hash for the version
    response_content: list[dict] = response.json()
    if not response_content:
        raise Sha1NotFoundError(
            f"SHA1 hash not found for version {original_version}. "
            "No tags found for repo.")

    # Sort the tags by version number
    for tag in response_content:
        tag_name: str = tag["ref"]
        tag_name: str = (tag_name.strip("refs/tags/").strip("-")
                         .strip("v").strip("@40"))
        tag["ref"] = tag_name
        tag_digits = "".join([c for c in tag_name if c.isdigit()])

        if not tag_digits:
            tag_digits = inf
        else:
            tag_digits = int(tag_digits)

        tag["tag_digits"] = tag_digits

    response_content = sorted(response_content,
                              key=lambda x: x["tag_digits"], reverse=True)

    # Get the SHA1 hash for the version
    version_digits = "".join([c for c in version if c.isdigit()])
    if version_digits:
        version_digits = int(version_digits)

    result_sha1 = ""

    for tag in response_content:
        tag_name: str = tag["ref"]
        tag_sha: str = tag["object"]["sha"]

        # Check if the tag name contains the version
        if version in tag_name:
            result_sha1 = tag_sha
            break

        if not version_digits:
            continue

        tag_digits = tag["tag_digits"]

        # Check if the tag version is less than or equal to the required
        # version
        if tag_digits <= version_digits:
            result_sha1 = tag_sha
            break

    if result_sha1:
        assert is_valid_sha1(result_sha1)
        return result_sha1

    raise Sha1NotFoundError(
        f"SHA1 hash not found for version {original_version}.")


def is_valid_sha1(sha1_str: str) -> bool:
    """
    Check the validity of a sha1 string.

    Args:
        sha1_str (str): The SHA1 string to validate.

    Returns:
        bool: True if the SHA1 string is valid, False otherwise.
    """
    if not re.match('^[0-9A-Fa-f]{40}$', sha1_str):
        return False
    return True


def get_github_token() -> str:
    """
    Gets the GitHub authentication token from the environment.

    Returns:
        str: The GitHub authentication token.

    Raises:
        ValueError: If the GitHub authentication token is not found in the
        environment.
    """
    token = os.environ.get('GITHUB_AUTH_TOKEN')
    if not token:
        raise ValueError(
            "GitHub authentication token not found in environment"
            )
    return token
