"""
This file contains test cases for the `calculate_final_scores` function in the `calculator` module.
"""

from src.final_score_calculator.calculator import calculate_final_scores
from src.util import Dependency

def test_calculate_final_scores_empty_dependencies():
    """Test when dependencies list is empty"""
    dependencies = []
    expected_scores = []
    assert calculate_final_scores(dependencies) == expected_scores

def test_calculate_final_scores_single_dependency():
    """Test when there is only one dependency"""
    dependencies = [
        Dependency(url="https://example.com", dependency_score={"checks": [
            {"name": "check1", "score": 5},
            {"name": "check2", "score": 3},
            {"name": "check3", "score": 7}
        ]})
    ]
    expected_scores = [
        ["check1", 5, "https://example.com"],
        ["check2", 3, "https://example.com"],
        ["check3", 7, "https://example.com"]
    ]
    assert calculate_final_scores(dependencies) == expected_scores

def test_calculate_final_scores_multiple_dependencies():
    """Test when there are multiple dependencies"""
    dependencies = [
        Dependency(url="https://example.com", dependency_score={"checks": [
            {"name": "check1", "score": 5},
            {"name": "check2", "score": 3},
            {"name": "check3", "score": 7}
        ]}),
        Dependency(url="https://example.org", dependency_score={"checks": [
            {"name": "check1", "score": 2},
            {"name": "check2", "score": 4},
            {"name": "check3", "score": 6}
        ]}),
        Dependency(url="https://example.net", dependency_score={"checks": [
            {"name": "check1", "score": 8},
            {"name": "check2", "score": 1},
            {"name": "check3", "score": 9}
        ]})
    ]
    expected_scores = [
        ["check1", 2, "https://example.org"],
        ["check2", 1, "https://example.net"],
        ["check3", 6, "https://example.org"]
    ]
    assert calculate_final_scores(dependencies) == expected_scores
