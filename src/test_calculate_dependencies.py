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
import unittest
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


class TestCalculateDependencies(unittest.TestCase):
    """Test case for the calculate_dependencies module."""

    def test_parse_git_url(self):
        """Test the parse_git_url function."""
        url = "https://github.com/owner/repo"
        platform, repo_owner, repo_name = parse_git_url(url)
        self.assertEqual(platform, "github.com")
        self.assertEqual(repo_owner, "owner")
        self.assertEqual(repo_name, "repo")

    def test_get_component_url(self):
        """Test the get_component_url function."""
        component = {
            "externalReferences": [
                {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
            ]
        }
        url = get_component_url(component)
        self.assertEqual(url, "https://github.com/OSSQA-PUM/OSSQA")

    def test_parse_component(self):
        """Test the parse_component function."""
        component = {
            "externalReferences": [
                {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
            ]
        }
        dependency = parse_component(component)
        self.assertEqual(dependency.platform, "github.com")
        self.assertEqual(dependency.repo_owner, "OSSQA-PUM")
        self.assertEqual(dependency.repo_name, "OSSQA")

    def test_parse_sbom(self):
        """Test the parse_sbom function."""
        sbom = {"components": []}
        dependencies, failures, failure_reason = parse_sbom(sbom)
        self.assertEqual(len(dependencies), 0)
        self.assertEqual(len(failures), 0)
        self.assertEqual(len(failure_reason), 0)

    def test_get_git_sha1_number(self):
        """Test the get_git_sha1_number function."""
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        sha1 = get_git_sha1_number(dependency)
        self.assertIsNone(sha1)

    def test_try_get_from_ssf_api(self):
        """Test the try_get_from_ssf_api function."""
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        scorecard = try_get_from_ssf_api(dependency)
        self.assertIsNone(scorecard)

    def test_lookup_database(self):
        """Test the lookup_database function."""
        dependencies = [
            Dependency(
                json_component={},
                platform="github.com",
                repo_owner="owner",
                repo_name="repo1",
            ),
            Dependency(
                json_component={},
                platform="github.com",
                repo_owner="owner",
                repo_name="repo2",
            ),
        ]
        dependencies_with_scores, new_needed_dependencies = lookup_database(
            dependencies
        )
        self.assertEqual(len(dependencies_with_scores), 0)
        self.assertEqual(len(new_needed_dependencies), 2)

    def test_lookup_ssf(self):
        """Test the lookup_ssf function."""
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        scorecard = lookup_ssf(dependency)
        self.assertIsNone(scorecard)

    def test_lookup_multiple_ssf(self):
        """Test the lookup_multiple_ssf function."""
        dependencies = [
            Dependency(
                json_component={},
                platform="github.com",
                repo_owner="owner",
                repo_name="repo1",
            ),
            Dependency(
                json_component={},
                platform="github.com",
                repo_owner="owner",
                repo_name="repo2",
            ),
        ]
        dependencies_with_scores, new_needed_dependencies = lookup_multiple_ssf(
            dependencies
        )
        self.assertEqual(len(dependencies_with_scores), 0)
        self.assertEqual(len(new_needed_dependencies), 2)


if __name__ == "__main__":
    unittest.main()
