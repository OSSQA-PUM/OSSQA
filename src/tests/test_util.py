"""
Test cases for util.py
"""

import json
from pathlib import Path
import pytest
from tests.decorators import log_test_results
from util import Dependency, contains_all_checks, \
validate_scorecard, Checks


@pytest.fixture
def fixture_dependency():
    """
    Fixture for dependency.
    """
    json_component = {"name": "dependency", "version": "1.0"}
    platform = "github.com"
    repo_path = "/user/repo"
    url = "https://github.com/user/repo"
    failure_reason = None
    dependency_score = {
        "checks": [
            {"name": "Binary-Artifacts", "score": -1},
            {"name": "Branch-Protection", "score": 2},
            {"name": "CI-Tests", "score": 3},
            {"name": "CII-Best-Practices", "score": 4},
            {"name": "Code-Review", "score": 5},
            {"name": "Contributors", "score": 6},
            {"name": "Dangerous-Workflow", "score": 7},
            {"name": "Dependency-Update-Tool", "score": 8},
            {"name": "Fuzzing", "score": 9},
            {"name": "License", "score": 10},
            {"name": "Maintained", "score": 9},
            {"name": "Packaging", "score": 8},
            {"name": "Pinned-Dependencies", "score": 7},
            {"name": "SAST", "score": 6},
            {"name": "Security-Policy", "score": 5},
            {"name": "Signed-Releases", "score": 4},
            {"name": "Token-Permissions", "score": 3},
            {"name": "Vulnerabilities", "score": 2},
        ]
    }

    dependency = Dependency(json_component,
                            platform,
                            repo_path,
                            url,
                            failure_reason,
                            dependency_score)
    return dependency


@log_test_results([])  # TODO add relevant test case
def test_dependency_creation():
    """
    Test case for dependency creation.
    """
    json_component = {"name": "dependency", "version": "1.0"}
    platform = "github.com"
    repo_path = "/user/repo"
    url = "https://github.com/user/repo"
    failure_reason = None
    dependency_score = {"security": 5, "maintainability": 4}

    dependency = Dependency(json_component,
                            platform,
                            repo_path,
                            url,
                            failure_reason,
                            dependency_score)

    assert dependency.json_component == json_component
    assert dependency.platform == platform
    assert dependency.repo_path == repo_path
    assert dependency.url == url
    assert dependency.failure_reason == failure_reason
    assert dependency.dependency_score == dependency_score


@log_test_results([])  # TODO add relevant test case
def test_checks_enum(fixture_dependency: Dependency):
    """
    Test case for checks enum.
    """
    all_checks = Checks.all()
    for check in fixture_dependency.dependency_score["checks"]:
        assert check["name"] in all_checks


@log_test_results([])  # TODO add relevant test case
def test_dependency_get_check(fixture_dependency):
    """
    Test case for dependency get check.
    """
    assert fixture_dependency.get_check(Checks.BINARY_ARTIFACTS)["score"] == -1
    assert fixture_dependency.get_check(Checks.BINARY_ARTIFACTS)["name"] == Checks.BINARY_ARTIFACTS


@log_test_results([])  # TODO add relevant test case
def test_contains_all_checks(fixture_dependency):
    """
    Test case for checking if all checks are present.
    """
    dependency_score = fixture_dependency.dependency_score
    assert contains_all_checks(dependency_score["checks"])
    del dependency_score["checks"][0]
    assert not contains_all_checks(dependency_score["checks"])


@log_test_results([])  # TODO add relevant test case
def test_validate_scorecard(fixture_dependency):
    """
    Test case for validating the scorecard.
    """
    dependency_score = fixture_dependency.dependency_score
    assert validate_scorecard(dependency_score)
    del dependency_score["checks"][0]
    assert not validate_scorecard(dependency_score)
    dependency_score["checks"].append({"name": "radom-score", "score": -1})
    assert not validate_scorecard(dependency_score)

    dependency_score = fixture_dependency.dependency_score
    del dependency_score["checks"][0]["score"]
    assert not validate_scorecard(dependency_score)

    ssf_scorecard_path = str(Path(__file__).parent.parent.absolute() \
                             / "final_score_calculator" \
                             / "example_response.json")
    with open(ssf_scorecard_path, "r", encoding="utf-8") as file:
        dependency_score = json.load(file)
    assert validate_scorecard(dependency_score)


if __name__ == "__main__":
    pytest.main()