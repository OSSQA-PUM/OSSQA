import pytest
from data_types.dependency_scorer import SSFAPIFetcher, ScorecardAnalyzer

DUMMY_DEPS = [
    {
        "name": "github.com/
        "version": "1.0"
    },
    {
        "name": "dep2",
        "version": "2.0"
    }
]

@pytest.fixture(params=)

def test_scorecard_analyzer():
    analyzer = ScorecardAnalyzer(lambda x: None)
    analyzer.score([])
    assert analyzer is not None
    assert analyzer.fetcher is not None
    assert analyzer.fetcher == fetcher
    assert analyzer.analyze is not None
    assert analyzer.analyze == fetcher.score
    assert analyzer.analyze == analyzer.fetcher.score
    assert analyzer.analyze == analyzer.fetch