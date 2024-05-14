"""
This file contains test cases for the Dependency class.

The Dependency class represents a single dependency in a software bill of
materials (SBOM). It contains information about the dependency, such as its
name, version, and scorecard. The class provides methods for initializing a
dependency, comparing dependencies, and converting dependencies to a
dictionary representation.
"""

import json
import re
import pytest
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from tests.main.unit.scorecards.scorecards import PATHS
from tests.main.unit.sboms.sboms import DUMMY_DEPENDENCIES

DEPENDENCY_NAME = "github.com/repo/path"
COMPONENT_NAME = "path"



@pytest.fixture
def dependency_basic():
    """
    Fixture to create a basic Dependency object.
    """
    return Dependency(
        DUMMY_DEPENDENCIES[0]
        )


@pytest.fixture(params=PATHS)
def dependency_scorecard(request):
    """
    Fixture to create a Dependency object with a scorecard.
    """
    with open(request.param, "r", encoding="utf-8") as file:
        scorecard = json.load(file)
    dep = Dependency(DUMMY_DEPENDENCIES[0])
    dep.scorecard = Scorecard(scorecard)
    return dep


def test_dependency_initialization():
    """
    Test that a Dependency object can be initialized.
    """
    assert Dependency(DUMMY_DEPENDENCIES[0])


def test_dependency_eq():
    """
    Test that two Dependency objects are equal if they have the same name
    and version."""
    dep1 = Dependency(DUMMY_DEPENDENCIES[0])
    dep2 = Dependency(DUMMY_DEPENDENCIES[0])
    assert dep1 == dep2


def test_dependency_not_eq():
    """
    Test that two Dependency objects are not equal if they have different
    names or versions."""
    dep1 = Dependency(DUMMY_DEPENDENCIES[0])
    dep2 = Dependency(DUMMY_DEPENDENCIES[1])
    dep3 = Dependency(DUMMY_DEPENDENCIES[2])
    dep4 = Dependency(DUMMY_DEPENDENCIES[3])
    dep5 = Dependency(DUMMY_DEPENDENCIES[4])
    assert dep1 != dep2
    assert dep1 != dep3
    assert dep1 != dep4
    assert dep4 != dep5


def test_dependency_platform(dependency_basic):
    """
    Test that the platform property of a Dependency object is correct.
    """
    assert dependency_basic.platform == "github.com"


def test_dependency_repo_path(dependency_basic):
    """
    Test that the repo_path property of a Dependency object is correct.
    """
    assert isinstance(dependency_basic.repo_path, str)
    assert len(dependency_basic.repo_path) > 0
    assert "/" in dependency_basic.repo_path
    assert re.search(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$",
                     dependency_basic.repo_path)


def test_dependency_url(dependency_basic):
    """
    Test that the url property of a Dependency object is correct.
    """
    assert isinstance(dependency_basic.git_url, str)
    assert len(dependency_basic.git_url) > 0
    assert "/" in dependency_basic.git_url
    assert re.search(r"https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$",
                     dependency_basic.git_url)


def test_dependency_basic_to_dict(dependency_basic):
    """
    Test that the to_dict method of a Dependency object returns the correct
    dictionary representation of the object.
    """
    dep_dict = dependency_basic.to_dict()
    assert "scorecard" in dep_dict
    assert "failure_reason" in dep_dict
    for key in DUMMY_DEPENDENCIES[0]:
        assert key in dep_dict
        assert dep_dict[key] == DUMMY_DEPENDENCIES[0][key]


def test_dependency_scorecard_to_dict(dependency_scorecard):
    """
    Test that the to_dict method of a Dependency object with a scorecard
    returns the correct dictionary representation of the object.
    """
    dep_dict = dependency_scorecard.to_dict()
    assert "scorecard" in dep_dict
    assert "failure_reason" in dep_dict
    for key in DUMMY_DEPENDENCIES[0]:
        assert key in dep_dict
        assert dep_dict[key] == DUMMY_DEPENDENCIES[0][key]

    # Check correct format of scorecard
    assert isinstance(dep_dict["scorecard"], dict)
    assert "date" in dep_dict["scorecard"]
    assert "score" in dep_dict["scorecard"]
    assert "checks" in dep_dict["scorecard"]
    assert isinstance(dep_dict["scorecard"]["date"], str)
    assert isinstance(dep_dict["scorecard"]["score"], float)
    assert isinstance(dep_dict["scorecard"]["checks"], list)
    assert all(
        isinstance(check, dict)
        for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        "name" in check for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        "score" in check for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        "reason" in check for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        "details" in check for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        isinstance(check["name"], str)
        for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        isinstance(check["score"], int)
        for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        isinstance(check["reason"], str)
        for check in dep_dict["scorecard"]["checks"]
        )
    assert all(
        isinstance(check["details"], list | None)
        for check in dep_dict["scorecard"]["checks"]
        )
