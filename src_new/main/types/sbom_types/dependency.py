"""
This module contains the Dependency class which represents a dependency for 
a project.
"""

from dataclasses import dataclass
from sbom_types.scorecard import Scorecard


@dataclass
class Dependency:
    """
    Represents a dependency for a project.

    Attributes:
        platform (str): The platform on which the dependency is used.
        repo_path (str): The path to the repo
        url (str): The URL of the dependency.
        failure_reason (Exception): The reason for any failure 
                                    related to the dependency.
        dependency_score (Scorecard): The scorecard related to the dependency.
    """
    platform: str = None
    repo_path: str = None
    url: str = None
    version: str = None
    dependency_score: Scorecard = None
    failure_reason: Exception = None

    def __eq__(self, other):
        """
        Check if two dependencies are equal.

        Args:
            other (Dependency): The other dependency to compare with.

        Returns:
            bool: True if the dependencies are equal, False otherwise.
        """
        return self.platform == other.platform and \
        self.repo_path == other.repo_path and self.version == other.version

    def to_dict(self) -> dict:
        """
        Convert the dependency to a dictionary.

        Returns:
            dict: The dictionary representation of the dependency.
        """
        return {
            "platform": self.platform,
            "url": self.url,
            "repo_path": self.repo_path,
            "version": self.version,
            "dependency_score": self.dependency_score.to_dict() \
                if self.dependency_score else "",

            "failure_reason": self.failure_reason \
                if self.failure_reason else ""
        }
