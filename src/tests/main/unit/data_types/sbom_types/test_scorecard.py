"""
Test the Scorecard class and its methods.

The Scorecard class represents a scorecard retrieved from OpenSSF Scorecard.
It contains information about the scorecard, such as the date, score,
and checks. The class provides methods for initializing a scorecard, converting
the scorecard to a dictionary representation, and validating the scorecard.
"""

import json
import pytest
from main.data_types.sbom_types.scorecard import Scorecard, ScorecardChecks
from tests.main.unit.scorecards.scorecards import (PATHS,
                                                   UNPARSABLE_SCORECARDS,
                                                   OUT_OF_BOUNDS_SCORECARDS)


@pytest.fixture(params=UNPARSABLE_SCORECARDS)
def scorecard_json_unparsable(request):
    """
    Fixture to load an unparsable scorecard JSON file.
    """
    return request.param


@pytest.fixture(params=OUT_OF_BOUNDS_SCORECARDS)
def scorecard_json_out_of_bounds(request):
    """
    Fixture to load a scorecard JSON file with a score that is out of bounds.
    """
    return request.param


@pytest.fixture(params=PATHS)
def scorecard_json(request):
    """
    Fixture to load a scorecard JSON file.
    """
    with open(request.param, "r", encoding="utf-8") as file:
        return json.load(file)


def test_scorecard_initialization(scorecard_json):
    """
    Test that a scorecard can be initialized.
    """
    assert Scorecard(scorecard_json)


def test_scorecard_to_dict(scorecard_json):
    """
    Test that the to_dict method returns a dictionary representation of the
    scorecard.
    """
    scorecard = Scorecard(scorecard_json)
    scorecard_dict = scorecard.to_dict()
    assert "date" in scorecard_dict
    assert "score" in scorecard_dict
    assert "checks" in scorecard_dict
    assert isinstance(scorecard_dict["date"], str)
    assert isinstance(scorecard_dict["score"], float)
    assert isinstance(scorecard_dict["checks"], list)
    assert all(isinstance(check, dict) for check in scorecard_dict["checks"])
    assert all("name" in check for check in scorecard_dict["checks"])
    assert all("score" in check for check in scorecard_dict["checks"])
    assert all("reason" in check for check in scorecard_dict["checks"])
    assert all("details" in check for check in scorecard_dict["checks"])
    assert all(
        isinstance(check["name"], str) for check in scorecard_dict["checks"]
        )
    assert all(
        isinstance(check["score"], int) for check in scorecard_dict["checks"]
        )
    assert all(
        isinstance(check["reason"], str) for check in scorecard_dict["checks"]
        )
    assert all(
        isinstance(check["details"], list | None)
        for check in scorecard_dict["checks"]
        )


def test_unparsable_scorecard(scorecard_json_unparsable):
    with pytest.raises(AssertionError):
        Scorecard(scorecard_json_unparsable)


def test_out_of_bounds_scorecard(scorecard_json_out_of_bounds):
    """
    Test that a ValueError is raised when a scorecard has a score that is out
    of bounds.
    """
    with pytest.raises(AssertionError):
        Scorecard(scorecard_json_out_of_bounds)


def test_scorecard_equals():
    """
    Test that two scorecards are equal when they have the same values.

    This test uses the same scorecard JSON file for both scorecards.
    """
    with open(PATHS[0], "r") as file:
        json_dict = json.load(file)
    scorecard1 = Scorecard(json_dict)
    scorecard2 = Scorecard(json_dict)
    assert scorecard1 == scorecard2


def test_scorecard_not_equals():
    """
    Test that two scorecards are not equal when they have different values.

    This test uses two different scorecard JSON files for the scorecards.
    """
    with open(PATHS[0], "r") as file:
        scorecard1 = json.load(file)
    with open(PATHS[1], "r") as file:
        scorecard2 = json.load(file)
    scorecard1 = Scorecard(scorecard1)
    scorecard2 = Scorecard(scorecard2)
    assert scorecard1 != scorecard2


def test_check_title_hyphen_to_snake():
    """
    Test that the title_hyphen_to_snake method replaces hyphens with
    underscores and converts the title to lowercase.
    """
    for check in ScorecardChecks.all():
        snake = ScorecardChecks.title_hyphen_to_snake(check)
        assert "-" not in snake
        assert snake.islower()
