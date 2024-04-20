"""
This module contains the classes for the scorecards created from SSFScorecards.

Classes:
- Check: Represents a check on a dependency.
- Scorecard: Represents a scorecard for a dependency.
- ScorecardChecks: Represents the checks that can be performed on a dependency.
"""

from dataclasses import dataclass, asdict
from enum import StrEnum


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
    Represents a scorecard for a dependency.
    https://securityscorecards.dev/#the-checks
    """
    date: str
    score: float
    checks: list[Check]

    def __init__(self, ssf_scorecard: dict):
        """
        Initializes the scorecard.

        Args:
            ssf_scorecard (dict): The SSF scorecard.
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

    def _validate(self, ssf_scorecard: dict) -> None:
        """
        Validates the scorecard.

        Returns:
            bool: True if the scorecard is valid, False otherwise.
        """
        if not isinstance(ssf_scorecard, dict):
            raise TypeError("Scorecard must be a dictionary.")
        
        if "date" not in ssf_scorecard:
            raise KeyError("Scorecard must contain a date.")
        
        if "score" not in ssf_scorecard:
            raise KeyError("Scorecard must contain a score.")
        score = ssf_scorecard.get("score")
        if not 0 <= score <= 10:
            raise ValueError("Score must be between 0 and 10.")
        
        if "checks" not in ssf_scorecard:
            raise KeyError("Scorecard must contain checks.")
        checks = ssf_scorecard.get("checks")
        for check in checks:
            if not isinstance(check, dict):
                raise TypeError("Check must be a dictionary.")
            
            if "name" not in check:
                raise KeyError("Check must contain a name.")
            
            if "score" not in check:
                raise KeyError("Check must contain a score.")
            if not -1 <= check.get("score") <= 10:
                raise ValueError("Check score must be between -1 and 10.")
            
            if "reason" not in check:
                raise KeyError("Check must contain a reason.")
            
            if "details" not in check:
                raise KeyError("Check must contain details.")

    def to_dict(self) -> dict:
        """
        Converts the scorecard to a dictionary.

        Returns:
            dict: The scorecard as a dictionary.
        """
        return asdict(self)


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

"""