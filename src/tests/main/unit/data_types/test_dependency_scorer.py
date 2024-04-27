
import json
import pytest
from main.data_types.dependency_scorer import ScorecardAnalyzer
from main.data_types.sbom_types.scorecard import Scorecard
from tests.main.unit.scorecards.scorecards import PATHS

# Dummy dependencies for testing
DUMMY_DEPS = [
    {
        "name": "github.com/",
        "version": "1.0"
    },
    {
        "name": "dep2",
        "version": "2.0"
    }
]


@pytest.fixture(params=PATHS)
def git_hub_sha1(request):
    with open(request.param, "r", encoding="utf-8") as file:
        scorecard = json.load(file)
    git_url = scorecard["repo"]["name"]
    commit = scorecard["repo"]["commit"]
    checks = scorecard["checks"]
    return (git_url, commit, checks)


@pytest.mark.skip("ScorecardAnalyzer tests are not implemented")
def test_scorecard_analyzer(git_hub_sha1):
    analyzer = ScorecardAnalyzer(lambda x: None)
    git_url, commit, checks = git_hub_sha1
    result: Scorecard = analyzer._execute_scorecard(
        git_url, commit, timeout=15
    )
    assert Scorecard(checks) == result, \
        "Scorecard does not match expected result"
