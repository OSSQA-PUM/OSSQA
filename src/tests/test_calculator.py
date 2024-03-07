"""
This file contains test cases for the `calculate_final_scores` function in the `calculator` module.
"""
import pytest
import copy
from final_score_calculator.calculator import calculate_final_scores
from util import Dependency

@pytest.fixture
def fixture_dependency():
    """Fixture for a dependency"""
    json_component = {"name": "dependency", "version": "1.0"}
    platform = "github.com"
    repo_owner = "user"
    repo_name = "repo"
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
                            repo_owner,
                            repo_name,
                            url,
                            failure_reason,
                            dependency_score)
    return dependency

def test_calculate_final_scores_empty_dependencies():
    """Test when dependencies list is empty"""
    dependencies = []
    expected_scores = []
    assert calculate_final_scores(dependencies) == expected_scores

def test_calculate_final_scores_single_dependency(fixture_dependency):
    """Test when there is only one dependency"""
    dependencies = [
        fixture_dependency
    ]
    expected_scores = [
        [ "Binary-Artifacts", -1, "https://github.com/user/repo" ],
        [ "Branch-Protection", 2, "https://github.com/user/repo" ],
        [ "CI-Tests", 3, "https://github.com/user/repo" ],
        [ "CII-Best-Practices", 4, "https://github.com/user/repo" ],
        [ "Code-Review", 5, "https://github.com/user/repo" ],
        [ "Contributors", 6, "https://github.com/user/repo" ],
        [ "Dangerous-Workflow", 7, "https://github.com/user/repo" ],
        [ "Dependency-Update-Tool", 8, "https://github.com/user/repo" ],
        [ "Fuzzing", 9, "https://github.com/user/repo" ],
        [ "License", 10, "https://github.com/user/repo" ],
        [ "Maintained", 9, "https://github.com/user/repo" ],
        [ "Packaging", 8, "https://github.com/user/repo" ],
        [ "Pinned-Dependencies", 7, "https://github.com/user/repo" ],
        [ "SAST", 6, "https://github.com/user/repo" ],
        [ "Security-Policy", 5, "https://github.com/user/repo" ],
        [ "Signed-Releases", 4, "https://github.com/user/repo" ],
        [ "Token-Permissions", 3, "https://github.com/user/repo" ],
        [ "Vulnerabilities", 2, "https://github.com/user/repo" ],
    ]
    assert calculate_final_scores(dependencies) == expected_scores

def test_calculate_final_scores_multiple_dependencies(fixture_dependency):
    """Test when there are multiple dependencies"""

    dependency1 = copy.deepcopy(fixture_dependency)
    dependency2 = copy.deepcopy(fixture_dependency)
    dependency3 = copy.deepcopy(fixture_dependency)

    dependencies = [
        dependency1,
        dependency2,
        dependency3
    ]

    dependencies[1].url = "url2"
    dependencies[2].url = "url3"
    dependencies[1].dependency_score["checks"][0]["score"] = 0
    dependencies[1].dependency_score["checks"][1]["score"] = -1
    dependencies[1].dependency_score["checks"][5]["score"] = 7
    dependencies[2].dependency_score["checks"][0]["score"] = 1
    dependencies[2].dependency_score["checks"][3]["score"] = 1

    print(dependency2)

    expected_scores = [
        [ "Binary-Artifacts", -1, "https://github.com/user/repo" ],
        [ "Branch-Protection", -1, "url2" ],
        [ "CI-Tests", 3, "https://github.com/user/repo" ],
        [ "CII-Best-Practices", 1, "url3" ],
        [ "Code-Review", 5, "https://github.com/user/repo" ],
        [ "Contributors", 6, "https://github.com/user/repo" ],
        [ "Dangerous-Workflow", 7, "https://github.com/user/repo" ],
        [ "Dependency-Update-Tool", 8, "https://github.com/user/repo" ],
        [ "Fuzzing", 9, "https://github.com/user/repo" ],
        [ "License", 10, "https://github.com/user/repo" ],
        [ "Maintained", 9, "https://github.com/user/repo" ],
        [ "Packaging", 8, "https://github.com/user/repo" ],
        [ "Pinned-Dependencies", 7, "https://github.com/user/repo" ],
        [ "SAST", 6, "https://github.com/user/repo" ],
        [ "Security-Policy", 5, "https://github.com/user/repo" ],
        [ "Signed-Releases", 4, "https://github.com/user/repo" ],
        [ "Token-Permissions", 3, "https://github.com/user/repo" ],
        [ "Vulnerabilities", 2, "https://github.com/user/repo" ],
    ]
    assert calculate_final_scores(dependencies) == expected_scores
