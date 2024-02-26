import pytest
from prototype.prototype import analyze_dependency_score
from typing import List, Tuple

@pytest.fixture
def expected_scorecard_output() -> Tuple:
    return ('Binary-Artifacts', 
            'Branch-Protection', 
            'CI-Tests', 
            'CII-Best-Practices', 
            'Code-Review', 
            'Contributors', 
            'Dangerous-Workflow', 
            'Dependency-Update-Tool', 
            'Fuzzing', 
            'License', 
            'Maintained', 
            'Packaging', 
            'Pinned-Dependencies', 
            'SAST', 
            'Security-Policy', 
            'Signed-Releases', 
            'Token-Permissions', 
            'Vulnerabilities')

def test_analyze_dependency_score(expected_scorecard_output) -> None:
    # Tests the format of of the SSF scorecard analyser.
    
    git_urls = ["github.com/OSSQA-PUM/OSSQA"]

    list : List[Tuple[str, int, str]] = analyze_dependency_score(git_urls[0])
    assert len(list) == 18
    assert len(list[0]) == 3
    for item in list:
        assert item[0] in expected_scorecard_output



