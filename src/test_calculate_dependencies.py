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
    def test_parse_git_url(self):
        url = "https://github.com/owner/repo"
        platform, repo_owner, repo_name = parse_git_url(url)
        self.assertEqual(platform, "github.com")
        self.assertEqual(repo_owner, "owner")
        self.assertEqual(repo_name, "repo")

    def test_get_component_url(self):
        component = {
            "externalReferences": [
                {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
            ]
        }
        url = get_component_url(component)
        self.assertEqual(url, "https://github.com/OSSQA-PUM/OSSQA")

    def test_parse_component(self):
        component = {
            "externalReferences": [
                {"type": "vcs", "url": "https://github.com/OSSQA-PUM/OSSQA"}
            ]
        }
        dependency = parse_component(component)
        print(dependency)
        self.assertEqual(dependency.platform, "github.com")
        self.assertEqual(dependency.repo_owner, "OSSQA-PUM")
        self.assertEqual(dependency.repo_name, "OSSQA")

    def test_parse_sbom(self):
        sbom = {"components": []}
        dependencies, failures, failure_reason = parse_sbom(sbom)
        self.assertEqual(len(dependencies), 0)
        self.assertEqual(len(failures), 0)
        self.assertEqual(len(failure_reason), 0)

    def test_get_git_sha1_number(self):
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        sha1 = get_git_sha1_number(dependency)
        self.assertIsNone(sha1)

    def test_try_get_from_ssf_api(self):
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        scorecard = try_get_from_ssf_api(dependency)
        self.assertIsNone(scorecard)

    def test_lookup_database(self):
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
        dependency = Dependency(
            json_component={},
            platform="github.com",
            repo_owner="owner",
            repo_name="repo",
        )
        scorecard = lookup_ssf(dependency)
        self.assertIsNone(scorecard)

    def test_lookup_multiple_ssf(self):
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