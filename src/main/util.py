"""
This module contains utility functions for the main module.

Functions:
- get_git_sha1: Gets the SHA1 hash for a version of a dependency.
- is_valid_sha1: Check the validity of a sha1 string.
"""
import re


def get_git_sha1(self, git_url: str, version: str) -> str:
    """
    Gets the SHA1 hash for a version of a dependency.

    Args:
        git_url (str): The Git URL of the dependency.
        version (str): The version of the dependency.

    Returns:
        str: The SHA1 hash of the version.
    """
    sha1 = ""
    # TODO
    # Add function to get git sha1 number'
    
    assert is_valid_sha1(sha1), f"given commit sha1: {sha1} is not valid"
    return sha1


def is_valid_sha1(sha1_str: str) -> bool:
    if not re.match('^[0-9A-Fa-f]{40}$', sha1_str):
        return False
    return True
