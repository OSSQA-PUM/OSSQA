import pytest
import json
from main.data_types.sbom_types.scorecard import Scorecard, ScorecardChecks
from tests.main.unit.scorecards.scorecards import PATHS, UNPARSABLE_SCORECARDS, OUT_OF_BOUNDS_SCORECARDS

@pytest.fixture(params=UNPARSABLE_SCORECARDS)
def scorecard_json_unparsable(request):
    return request.param

@pytest.fixture(params=OUT_OF_BOUNDS_SCORECARDS)
def scorecard_json_out_of_bounds(request):
    return request.param

@pytest.fixture(params=PATHS)
def scorecard_json(request):
    with open(request.param, "r") as file:
        return json.load(file)

def test_scorecard_initialization(scorecard_json):
    assert Scorecard(scorecard_json)

def test_scorecard_to_dict(scorecard_json):
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
    assert all(isinstance(check["name"], str) for check in scorecard_dict["checks"])
    assert all(isinstance(check["score"], int) for check in scorecard_dict["checks"])
    assert all(isinstance(check["reason"], str) for check in scorecard_dict["checks"])
    assert all(isinstance(check["details"], list | None) for check in scorecard_dict["checks"])

def test_unparsable_scorecard(scorecard_json_unparsable):
    with pytest.raises(KeyError):
        Scorecard(scorecard_json_unparsable)

def test_out_of_bounds_scorecard(scorecard_json_out_of_bounds):
    with pytest.raises(ValueError):
        Scorecard(scorecard_json_out_of_bounds)