"""
This module contains the classes for the scorecards created from SSFScorecards.

Classes:
- Check: Represents a check on a dependency.
- Scorecard: Represents a scorecard for a dependency.
- ScorecardChecks: Represents the checks that can be performed on a dependency.
"""

from dataclasses import dataclass, asdict
from enum import StrEnum
import json


class ScorecardChecks(StrEnum):
    """
    Represents the checks that can be performed on a dependency.
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

    @classmethod
    def all(cls):
        """
        Get all checks.

        Returns:
            list: A list of all checks.
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


@dataclass(frozen=True)
class Check:
    """
    Represents a check on a dependency.

    Attributes:
        score (int): The score of the check.
        reason (str): The reason for the score.
    """
    score: int
    reason: str


@dataclass
class Scorecard:
    """
    Represents a scorecard for a dependency.
    https://securityscorecards.dev/#the-checks
    """
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

    def __init__(self, ssf_scorecard: dict):
        """
        Initializes the scorecard.

        Args:
            ssf_scorecard (dict): The SSF scorecard.
        """
        for check in ssf_scorecard["checks"]:
            setattr(self, ScorecardChecks.title_hyphen_to_snake(check["name"]),
                    Check(check["score"], check["reason"]))

    def to_dict(self) -> dict:
        """
        Converts the scorecard to a dictionary.

        Returns:
            dict: The scorecard as a dictionary.
        """
        return {
            check.value: asdict(
                getattr(self, ScorecardChecks.title_hyphen_to_snake(check))
                ) for check in ScorecardChecks.all()
            }


if __name__== "__main__":
    default_check: Check = Check(10, "reason")
    with open("src/sbom/example_response.json") as f:
        example = json.loads(f.read())


    scorecard: Scorecard = Scorecard(example)
    print(scorecard)
