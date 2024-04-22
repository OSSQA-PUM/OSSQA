"""
This file contains test cases for the `calculate_final_scores` function in the `calculator` module.
"""
import copy
import pytest
from final_score_calculator.calculator import calculate_final_scores
from tests.decorators import log_test_results
from util import Dependency


@pytest.fixture
def fixture_dependency():
    """Fixture for a dependency"""
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


@log_test_results([2])
def test_calculate_final_scores_empty_dependencies():
    """Test when dependencies list is empty"""
    dependencies = []
    expected_scores = []
    assert calculate_final_scores(dependencies) == expected_scores
