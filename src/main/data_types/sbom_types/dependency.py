"""
This module contains the Dependency class which represents a dependency for
a project.
"""

from dataclasses import dataclass
from main.data_types.sbom_types.scorecard import Scorecard


@dataclass
class Dependency:
    """
    Represents a dependency for a project.

    Attributes:
        component_name (str): The name of the component.
        name (str): The name of the dependency, corresponds to the URL in
                    CycloneDX format.
        version (str): The version of the dependency.
        dependency_score (Scorecard): The scorecard related to the dependency.
        failure_reason (Exception): The reason for any failure
                                    related to the dependency.
    """
    component_name: str
    name: str
    version: str
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
        return self.name == other.name and self.version == other.version

    @property
    def platform(self) -> str:
        """
        Get the platform of the dependency.

        Returns:
            str: The platform of the dependency.
        """
        return self.name.split("/", maxsplit=1)[0]

    @property
    def repo_path(self) -> str:
        """
        Get the repo path of the dependency.

        Returns:
            str: The repo path of the dependency.
        """
        return self.name.split("/", maxsplit=1)[1]

    @property
    def url(self) -> str:
        """
        Get the URL of the dependency.

        Returns:
            str: The URL of the dependency.
        """
        return f"https://{self.name}"

    def to_dict(self) -> dict:
        """
        Convert the dependency to a dictionary.

        Returns:
            dict: The dictionary representation of the dependency.
        """
        return {
            "name": self.name,
            "version": self.version,
            "dependency_score": self.dependency_score.to_dict()
            if self.dependency_score else None,

            "failure_reason": str(self.failure_reason)
            if self.failure_reason else None
        }
