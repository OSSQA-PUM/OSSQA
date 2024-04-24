"""
This file contains test cases for the Dependency class.

The Dependency class represents a single dependency in a software bill of
materials (SBOM). It contains information about the dependency, such as its
name, version, and scorecard. The class provides methods for initializing a
dependency, comparing dependencies, and converting dependencies to a
dictionary representation.
"""

import json
import pytest
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from tests.main.unit.scorecards.scorecards import PATHS

DEPENDENCY_NAME = "github.com/repo/path"


@pytest.fixture
def dependency_basic():
    """
    Fixture to create a basic Dependency object.
    """
    return Dependency(name=DEPENDENCY_NAME, version="1.0")


@pytest.fixture(params=PATHS)
def dependency_scorecard(request):
    """
    Fixture to create a Dependency object with a scorecard.
    """
    with open(request.param, "r", encoding="utf-8") as file:
        scorecard = json.load(file)
    return Dependency(name=DEPENDENCY_NAME, version="1.0",
                      dependency_score=Scorecard(scorecard))


def test_dependency_initialization():
    """
    Test that a Dependency object can be initialized.
    """
    assert Dependency()


def test_dependency_eq():
    """
    Test that two Dependency objects are equal if they have the same name
    and version."""
    dep1 = Dependency(name="dep1", version="1.0")
    dep2 = Dependency(name="dep1", version="1.0")
    assert dep1 == dep2


def test_dependency_not_eq():
    """
    Test that two Dependency objects are not equal if they have different
    names or versions."""
    dep1 = Dependency(name="dep1", version="1.0")
    dep2 = Dependency(name="dep2", version="1.0")
    dep3 = Dependency(name="dep1", version="1.1")
    assert dep1 != dep2
    assert dep1 != dep3


def test_dependency_platform(dependency_basic):
    """
    Test that the platform property of a Dependency object is correct.
    """
    assert dependency_basic.platform == "github.com"


def test_dependency_repo_path(dependency_basic):
    """
    Test that the repo_path property of a Dependency object is correct.
    """
    assert dependency_basic.repo_path == "repo/path"


def test_dependency_url(dependency_basic):
    """
    Test that the url property of a Dependency object is correct.
    """
    assert dependency_basic.url == f"https://{DEPENDENCY_NAME}"


def test_dependency_basic_to_dict(dependency_basic):
    """
    Test that the to_dict method of a Dependency object returns the correct
    dictionary representation of the object.
    """
    dep_dict = dependency_basic.to_dict()
    assert "name" in dep_dict
    assert "version" in dep_dict
    assert dep_dict["name"] == DEPENDENCY_NAME
    assert dep_dict["version"] == "1.0"


def test_dependency_scorecard_to_dict(dependency_scorecard):
    """
    Test that the to_dict method of a Dependency object with a scorecard
    returns the correct dictionary representation of the object.
    """
    dep_dict = dependency_scorecard.to_dict()
    assert "name" in dep_dict
    assert "version" in dep_dict
    assert dep_dict["name"] == DEPENDENCY_NAME
    assert dep_dict["version"] == "1.0"
    assert "dependency_score" in dep_dict
    assert "failure_reason" in dep_dict

    # Check correct format of scorecard
    assert isinstance(dep_dict["dependency_score"], dict)
    assert "date" in dep_dict["dependency_score"]
    assert "score" in dep_dict["dependency_score"]
    assert "checks" in dep_dict["dependency_score"]
    assert isinstance(dep_dict["dependency_score"]["date"], str)
    assert isinstance(dep_dict["dependency_score"]["score"], float)
    assert isinstance(dep_dict["dependency_score"]["checks"], list)
    assert all(
        isinstance(check, dict)
        for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        "name" in check for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        "score" in check for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        "reason" in check for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        "details" in check for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        isinstance(check["name"], str)
        for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        isinstance(check["score"], int)
        for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        isinstance(check["reason"], str)
        for check in dep_dict["dependency_score"]["checks"]
        )
    assert all(
        isinstance(check["details"], list | None)
        for check in dep_dict["dependency_score"]["checks"]
        )
