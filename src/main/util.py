"""
This module contains utility functions for the main module.

Functions:
- get_git_sha1: Gets the SHA1 hash for a version of a dependency.
- is_valid_sha1: Check the validity of a sha1 string.
"""
import re
import os
import datetime
from time import time, sleep
import requests
from packaging import version as version_parser

def get_token_data() -> dict:
    """
    Returns:
        dict: A dictionary containing the user's GitHub API token data 
    """
    token = os.environ.get('GITHUB_AUTH_TOKEN')
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
            "time_until_reset": int(user_data["X-RateLimit-Reset"]) - time()
        }

    print(f"Failed to authenticate. Status code: {response.status_code}")
    return None

def get_git_sha1(git_url: str, version: str, name: str, check: str) -> str:
    """
    Gets the SHA1 hash for a version of a dependency.

    Args:
        git_url (str): The Git URL of the dependency.
        version (str): The version of the dependency.
        name (str): The name of the dependency.
        check (str): The type of check to perform. Either "release" or "tag".

    Returns:
        str: The SHA1 hash of the version.

    Raises:
        ValueError: If the version does not exist.
        AssertionError: If the SHA1 hash is invalid.
        ConnectionRefusedError: If the connection is refused.
    """
    def is_greater_than(v1: str, v2: str) -> bool:
        return version_parser.parse(v1) >= version_parser.parse(v2)

    def find_matching_release(release_tags: list[str], version: str) \
            -> str | None:
        """
        Finds the nearest release that is less than the given version.
        """
        # Remove "v" prefix and "-*" suffix from version
        version = re.sub(r'^v', '', version)
        version = re.sub(r'-.*$', '', version)

        try:
            # Sort the release tags in descending order
            release_tags.sort(
                key=lambda tag: version_parser.parse(tag),
                reverse=True
                )
        except version_parser.InvalidVersion:
            pass

        for tag in release_tags:
            # Remove "v" prefix and "-*" suffix from tag
            stripped_tag = re.sub(r'^v', '', tag)
            stripped_tag = re.sub(r'-.*$', '', stripped_tag)
            try:
                if is_greater_than(version, stripped_tag):
                    return tag
            except version_parser.InvalidVersion:
                pass
        return None

    # Get the GitHub authentication token
    token = os.environ.get('GITHUB_AUTH_TOKEN')
    if not token:
        raise ValueError(
            "GitHub authentication token not found in environment"
            )
    headers = {'Authorization': f'token {token}'} if token else {}

    # Check that the release version exists
    if check == "release":
        url = f"https://api.github.com/repos/{git_url}/releases/tags/{version}"
    elif check == "tag":
        url = f"https://api.github.com/repos/{git_url}/tags/{version}"
    response = requests.get(url, headers=headers, timeout=10)

    # Check if the rate limit is exceeded
    if response.status_code == 403 \
            and "API rate limit exceeded" in response.json()["message"]:
        reset_time = response.headers.get("X-RateLimit-Reset")

        wait_time: float = int(reset_time) - time()

        # Convert the reset time to a human-readable format
        reset_time = datetime.datetime.fromtimestamp(int(reset_time))
        reset_time = reset_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"GitHub API rate limit exceeded. Rate limit resets at {reset_time}.")
        sleep(wait_time + 10)
        return get_git_sha1(git_url=git_url,
                            version=version,
                            name=name,
                            check=check)

    # Check if the response is successful
    if response.status_code != 200:
        # Try to get all releases and find the matching nearest release
        # that is less than the given version
        if check == "release":
            url = f"https://api.github.com/repos/{git_url}/releases"
        elif check == "tag":
            url = f"https://api.github.com/repos/{git_url}/tags"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"Failed to get release tags for {git_url}")
        if check == "release":
            tag_names = [release["tag_name"] for release in response.json()]
        elif check == "tag":
            tag_names = [release["name"] for release in response.json()]
        release_tag = find_matching_release(tag_names, version)

        # If no release found, try setting it to exact version
        if not release_tag:
            release_tag = version
    else:
        if check == "release":
            release_tag = response.json()["tag_name"]
        elif check == "tag":
            release_tag = response.json()["name"]

    try:
        # Get the commit SHA1 hash for the release tag
        url = f"https://api.github.com/repos/{git_url}/git/ref/tags/{release_tag}"
        reponse = requests.get(url, headers=headers, timeout=10)
        sha1 = ""
        if reponse.status_code == 200:
            sha1 = reponse.json()["object"]["sha"]

        assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
    except AssertionError:
        try:
            # Get the commit SHA1 hash for the release tag
            url = f"https://api.github.com/repos/{git_url}/git/ref/tags/{name + "-" + release_tag}"
            reponse = requests.get(url, headers=headers, timeout=10)
            sha1 = ""
            if reponse.status_code == 200:
                sha1 = reponse.json()["object"]["sha"]

            assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
        except AssertionError:
            try:
                # Get the commit SHA1 hash for the release tag
                url = (f"https://api.github.com/repos/{git_url}/git/ref/tags/"
                       f"{name + "-v" + release_tag}")
                reponse = requests.get(url, headers=headers, timeout=10)
                sha1 = ""
                if reponse.status_code == 200:
                    sha1 = reponse.json()["object"]["sha"]

                assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
            except AssertionError:
                try:
                    # Get the commit SHA1 hash for the release tag
                    url = f"https://api.github.com/repos/{git_url}/git/ref/tags/{"v" + release_tag}"
                    reponse = requests.get(url, headers=headers, timeout=10)
                    sha1 = ""
                    if reponse.status_code == 200:
                        sha1 = reponse.json()["object"]["sha"]

                    assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
                except AssertionError:
                    try:
                        # Get the commit SHA1 hash for the release tag
                        url = (f"https://api.github.com/repos/{git_url}/git/ref/tags/"
                               f"{name + "@40" + release_tag}")
                        reponse = requests.get(url, headers=headers, timeout=10)
                        sha1 = ""
                        if reponse.status_code == 200:
                            sha1 = reponse.json()["object"]["sha"]

                        assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
                    except AssertionError:
                        try:
                            # Get the commit SHA1 hash for the release tag
                            url = (f"https://api.github.com/repos/{git_url}/git/ref/tags/"
                                   f"{name + "@40v" + release_tag}")
                            reponse = requests.get(url, headers=headers, timeout=10)
                            sha1 = ""
                            if reponse.status_code == 200:
                                sha1 = reponse.json()["object"]["sha"]

                            assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
                        except AssertionError as e:
                            raise AssertionError((f"Failed to get commit SHA1 hash for "
                                                  f"{release_tag}")) from e
    return sha1

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
    """
    token = os.environ.get('GITHUB_AUTH_TOKEN')
    if not token:
        raise ValueError(
            "GitHub authentication token not found in environment"
            )
    return token


def raise_github_token_refused(response: requests.Response) -> None:
    """
    Raises an error if the GitHub API rate limit is exceeded.
    """
    reset_time = response.headers.get("X-RateLimit-Reset")

    # Convert the reset time to a human-readable format
    reset_time = datetime.datetime.fromtimestamp(int(reset_time))
    reset_time = reset_time.strftime("%Y-%m-%d %H:%M:%S")

    raise ConnectionRefusedError(
        (f"GitHub API rate limit exceeded. Try again later. "
            f"Rate limit resets at {reset_time}.")
            )
