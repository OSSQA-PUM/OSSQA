import pytest
from src.util import Dependency, check_token_usage

def test_dependency_creation():
    """
    Test case for dependency creation.
    """
    json_component = {"name": "dependency", "version": "1.0"}
    platform = "github.com"
    repo_owner = "user"
    repo_name = "repo"
    url = "https://github.com/user/repo"
    failure_reason = None
    dependency_score = {"security": 5, "maintainability": 4}

    dependency = Dependency(json_component,
                            platform,
                            repo_owner,
                            repo_name,
                            url,
                            failure_reason,
                            dependency_score)

    assert dependency.json_component == json_component
    assert dependency.platform == platform
    assert dependency.repo_owner == repo_owner
    assert dependency.repo_name == repo_name
    assert dependency.url == url
    assert dependency.failure_reason == failure_reason
    assert dependency.dependency_score == dependency_score

def test_bad_dependency_creation():
    """
    Test case for bad dependency creation.
    """
    try:
        dependency = Dependency()
    except TypeError:
        assert False

def test_check_token_usage():
    """
    Test case for checking token usage.
    """
    check_token_usage()
    

if __name__ == "__main__":
    pytest.main()
