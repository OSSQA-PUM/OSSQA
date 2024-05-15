"""
This module contains classes that represent data from OpenSSF Scorecard
results.

Classes:
- Check: Represents a scorecard check.
- Scorecard: Represents the results of OpenSSF Scorecard.
- ScorecardChecks: Represents the checks that can be performed by OpenSSF
Scorecard on a dependency.
"""

from dataclasses import dataclass, asdict
from enum import StrEnum


class ScorecardChecks(StrEnum):
    """
    Represents the checks that can be performed by OpenSSF Scorecard
    on a dependency.
    https://securityscorecards.dev/#the-checks
    """
    BINARY_ARTIFACTS = "Binary-Artifacts"
    BRANCH_PROTECTION = "Branch-Protection"
    CI_TESTS = "CI-Tests"
    CII_BEST_PRACTICES = "CII-Best-Practices"
    CODE_REVIEW = "Code-Review"
    CONTRIBUTORS = "Contributors"
    DANGEROUS_WORKFLOW = "Dangerous-Workflow"
    DEPENDENCY_UPDATE_TOOL = "Dependency-Update-Tool"
    FUZZING = "Fuzzing"
    LICENSE = "License"
    MAINTAINED = "Maintained"
    PACKAGING = "Packaging"
    PINNED_DEPENDENCIES = "Pinned-Dependencies"
    SAST = "SAST"
    SECURITY_POLICY = "Security-Policy"
    SIGNED_RELEASES = "Signed-Releases"
    TOKEN_PERMISSIONS = "Token-Permissions"
    VULNERABILITIES = "Vulnerabilities"
    WEBHOOKS = "Webhooks"

    @classmethod
    def all(cls):
        """
        Get all checks.

        Returns:
            list[ScorecardChecks]: The list of all checks.
        """
        return list(ScorecardChecks)

    @classmethod
    def title_hyphen_to_snake(cls, title: str) -> str:
        """
        Convert a title with hyphens to snake case.

        Args:
            title (str): The title to convert.

        Returns:
            str: The title in snake case.
        """
        return title.lower().replace("-", "_")


@dataclass(frozen=True, eq=True)
class Check:
    """
    Represents a scorecard check.

    Attributes:
        name (str): The name of the check.
        score (int): The score of the check.
        reason (str): The reason for the score.
        details (list[str]): The details of the check.
    """
    name: str
    score: int
    reason: str
    details: list[str]


@dataclass
class Scorecard:
    """
    Represents the results of OpenSSF Scorecard.
    https://securityscorecards.dev/#the-checks
    """
    date: str
    score: float
    checks: list[Check]
    """
        Old attributes for reference:
        binary_artifacts: Check
        branch_protection: Check
        ci_tests: Check
        cii_best_practices: Check
        code_review: Check
        contributors: Check
        dangerous_workflow: Check
        dependency_update_tool: Check
        fuzzing: Check
        license: Check
        maintained: Check
        packaging: Check
        pinned_dependencies: Check
        sast: Check
        security_policy: Check
        signed_releases: Check
        token_permissions: Check
        vulnerabilities: Check
    """

    def __init__(self, ssf_scorecard: dict):
        """
        Initializes the scorecard.

        Args:
            ssf_scorecard (dict): The OpenSSF Scorecard results.
        """
        self._validate(ssf_scorecard)
        self.date = ssf_scorecard["date"]
        self.score = ssf_scorecard["score"]
        self.checks = []
        for check in ssf_scorecard["checks"]:
            name = check["name"]
            score = check["score"]
            reason = check["reason"]
            details = check["details"]
            self.checks.append(Check(name, score, reason, details))

    def __eq__(self, other) -> bool:
        return isinstance(other, Scorecard) and \
            self.score == other.score and self.checks == other.checks

    def _validate(self, ssf_scorecard: dict) -> None:
        """
        Validates the scorecard.

        Args:
            ssf_scorecard (dict): The OpenSSF Scorecard results.

        Returns:
            bool: True if the scorecard is valid, False otherwise.

        Raises:
            AssertionError: If the scorecard is invalid.
        """
        assert isinstance(ssf_scorecard, dict), ("Scorecard must be a "
                                                 "dictionary.")

        assert "date" in ssf_scorecard, "Scorecard must contain a date."

        assert "score" in ssf_scorecard, "Scorecard must contain a score."
        score = ssf_scorecard.get("score")
        assert isinstance(score, (int, float)), "Score must be a number."
        assert -1 <= score <= 10, f"Score: {score} must be between -1 and 10."

        assert "checks" in ssf_scorecard, "Scorecard must contain checks."
        checks = ssf_scorecard.get("checks")
        assert isinstance(checks, list), "Checks must be a list."
        for check in checks:
            assert isinstance(check, dict), "Check must be a dictionary."

            assert "name" in check, "Check must contain a name."
            assert check.get("name") in ScorecardChecks.all(), \
                f"Check name '{check.get('name')}' not a valid check."

            assert "score" in check, "Check must contain a score."
            check_score = check.get("score")
            assert isinstance(check_score, (int, float)), \
                "Check score must be a number."
            assert -1 <= check_score <= 10, \
                "Check score must be between -1 and 10."

            assert "reason" in check, "Check must contain a reason."

            assert "details" in check, "Check must contain details."

    def to_dict(self) -> dict:
        """
        Creates a dictionary representing the scorecard.

        Returns:
            dict: The scorecard as a dictionary.
        """
        return asdict(self)
