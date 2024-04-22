import pytest
from data_types.dependency_scorer import SSFAPIFetcher, ScorecardAnalyzer

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


def test_scorecard_analyzer():
    analyzer = ScorecardAnalyzer(lambda x: None)
    analyzer.score([])
    assert analyzer is not None