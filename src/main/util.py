import requests

"""
This module contains utility functions for the main module.

Functions:
- get_git_sha1: Gets the SHA1 hash for a version of a dependency.
- is_valid_sha1: Check the validity of a sha1 string.
"""
import re
import requests
import os
from packaging import version as version_parser


# TODO: some repositories don't have release tags, only regular tags.
#       if there are no release tags, it should try to find a regular tag instead.
# TODO: what if there are not versions lower than the target version?
#       should it then grab to nearest larger version?
def get_git_sha1(git_url: str, version: str) -> str:
    """
    Gets the SHA1 hash for a version of a dependency.

    Args:
        git_url (str): The Git URL of the dependency.
        version (str): The version of the dependency.

    Returns:
        str: The SHA1 hash of the version.

    Raises:
        ValueError: If the version does not exist.
        AssertionError: If the SHA1 hash is invalid.
        ConnectionRefusedError: If the connection is refused.
    """
    def is_greater_than(v1: str, v2: str) -> bool:
        return version_parser.parse(v1) > version_parser.parse(v2)

    def find_matching_release(release_tags: list[str], version: str) \
            -> str | None:
        """
        Finds the nearest release that is less than the given version.
        """
        # Remove "v" prefix and "-*" suffix from version
        version = re.sub(r'^v', '', version)
        version = re.sub(r'-.*$', '', version)

        # Sort the release tags in descending order
        release_tags.sort(
            key=lambda tag: version_parser.parse(tag),
            reverse=True
            )

        for tag in release_tags:
            # Remove "v" prefix and "-*" suffix from tag
            stripped_tag = re.sub(r'^v', '', tag)
            stripped_tag = re.sub(r'-.*$', '', stripped_tag)
            if is_greater_than(version, stripped_tag):
                return tag
        return None

    # Get the GitHub authentication token
    token = os.environ.get('GITHUB_AUTH_TOKEN')
    if not token:
        raise ValueError(
            "GitHub authentication token not found in environment"
            )
    headers = {'Authorization': f'token {token}'} if token else {}

    # Check that the release version exists
    url = f"https://api.github.com/repos/{git_url}/releases/tags/{version}"
    response = requests.get(url, headers=headers, timeout=10)

    # Check if the response is successful
    if response.status_code != 200:
        # Try to get all releases and find the matching nearest release
        # that is less than the given version
        url = f"https://api.github.com/repos/{git_url}/releases"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"Failed to get release tags for {git_url}")
        tag_names = [release["tag_name"] for release in response.json()]
        release_tag = find_matching_release(tag_names, version)

        # Raise an error if no matching release less than the given version
        # is found
        if not release_tag:
            raise ValueError(f"Failed to find release tag for {version}")
    else:
        release_tag = response.json()["tag_name"]

    # Get the commit SHA1 hash for the release tag
    url = f"https://api.github.com/repos/{git_url}/git/ref/tags/{release_tag}"
    reponse = requests.get(url, headers=headers, timeout=10)
    sha1 = ""
    if reponse.status_code == 200:
        sha1 = reponse.json()["object"]["sha"]

    assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
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
