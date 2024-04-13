"""
This file contains unit tests for the calculate_dependencies module.
It tests various functions such as
`parse_git_url`, `get_component_url`, `parse_component`, `parse_sbom`,
`get_git_sha1_number`, `try_get_from_ssf_api`, `lookup_database`, `lookup_ssf`,
and `lookup_multiple_ssf`. Each test case verifies the functionality
and correctness of the corresponding function.

The unit tests cover different scenarios and edge cases
to ensure the robustness of the calculate_dependencies module.
The tests validate the parsing of Git URLs, retrieval of component URLs,
parsing of components, parsing of software bill of materials (SBOM),
retrieval of Git SHA1 numbers, querying the SSF API, database lookup,
and SSF lookup.

To run the unit tests, execute this file as the main module.
"""
import pytest
from calculate_dependencies import (
    Dependency,
    parse_git_url,
    get_component_url,
    parse_component,
    parse_sbom,
    get_git_sha1_number,
    try_get_from_ssf_api,
    lookup_database,
    lookup_ssf,
    lookup_multiple_ssf,
)
from tests.decorators import log_test_results


@log_test_results([3])
def test_parse_git_url():
    """Test the parse_git_url function."""
    url = "https://github.com/owner/repo"
    platform, repo_path = parse_git_url(url)
    assert platform == "github.com"
    assert repo_path == "/owner/repo"


@log_test_results([])  # TODO add relevant test case
def test_get_component_url():
    """Test the get_component_url function."""
    component = {
        "externalReferences": [
            {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
        ]
    }
    url = get_component_url(component)
    assert url == "https://github.com/OSSQA-PUM/OSSQA"


@log_test_results([3])
def test_parse_component():
    """Test the parse_component function."""
    component = {
        "externalReferences": [
            {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
        ]
    }
    dependency = parse_component(component)
    assert dependency.platform == "github.com"
    assert dependency.repo_path == "/OSSQA-PUM/OSSQA"


@log_test_results([3])
def test_parse_sbom():
    """Test the parse_sbom function."""
    sbom = {"components": []}
    dependencies, failures, failure_reason = parse_sbom(sbom)
    assert len(dependencies) == 0
    assert len(failures) == 0
    assert len(failure_reason) == 0


@log_test_results([])  # TODO add relevant test case
def test_get_git_sha1_number():
    """Test the get_git_sha1_number function."""
    dependency = Dependency(
        json_component={},
        platform="github.com",
        repo_path="/owner/repo"
    )
    sha1 = get_git_sha1_number(dependency)
    assert not sha1


@log_test_results([])  # TODO add relevant test case
def test_try_get_from_ssf_api():
    """Test the try_get_from_ssf_api function."""
    dependency = Dependency(
        json_component={},
        platform="github.com",
        repo_path="/owner/repo"
    )
    scorecard = try_get_from_ssf_api(dependency)
    assert scorecard is None


@pytest.mark.skip("This is an integration test, which is to be implemented later")
@log_test_results([])  # TODO add relevant test case
def test_lookup_database():
    """Test the lookup_database function."""
    dependencies = [
        Dependency(
            json_component={"name": "repo1", "version": "v1.0"},
            platform="github.com",
            repo_path="/owner/repo1",
        ),
        Dependency(
            json_component={"name": "repo2", "version": "v2.0"},
            platform="github.com",
            repo_path="/owner/repo2"
        ),
    ]
    dependencies_with_scores, new_needed_dependencies = lookup_database(dependencies)
    assert len(dependencies_with_scores) == 0
    assert len(new_needed_dependencies) == 2


@log_test_results([])  # TODO add relevant test case
def test_lookup_ssf():
    """Test the lookup_ssf function."""
    dependency = Dependency(
        json_component={},
        platform="github.com",
        repo_path="/owner/repo"
    )
    scorecard = lookup_ssf(dependency)
    assert scorecard is None


@log_test_results([])  # TODO add relevant test case
def test_lookup_multiple_ssf():
    """Test the lookup_multiple_ssf function."""
    dependencies = [
        Dependency(
            json_component={},
            platform="github.com",
            repo_path="/owner/repo1"
        ),
        Dependency(
            json_component={},
            platform="github.com",
            repo_path="/owner/repo2"
        ),
    ]
    dependencies_with_scores, new_needed_dependencies = lookup_multiple_ssf(dependencies)
    assert len(dependencies_with_scores) == 0
    assert len(new_needed_dependencies) == 2
