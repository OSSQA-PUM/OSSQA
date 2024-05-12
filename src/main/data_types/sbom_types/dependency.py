"""
This module contains the Dependency class which represents a dependency for
a project.
"""
from urllib.parse import urlparse
from re import search
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

    dependency_score: Scorecard = None
    failure_reason: Exception = None
    reach_requirement: str = None

    def __init__(self, dependency: dict):
        self.raw_component = dependency
        for dependency_attr in dependency:
            setattr(self, dependency_attr, dependency[dependency_attr])
        self.dependency_score = None
        self.failure_reason = None
        self.reach_requirement = False

    def __eq__(self, other):
        """
        Check if two dependencies are equal.

        Args:
            other (Dependency): The other dependency to compare with.

        Returns:
            bool: True if the dependencies are equal, False otherwise.
        """
        # Loop over all attributes of the dependency
        for attr in self.__dict__:
            # If the attribute is not the same in both dependencies
            if attr not in ("dependency_score", "failure_reason", "passed"):
                try:
                    other_attr = getattr(other, attr)
                except AttributeError:
                    return False
                if getattr(self, attr) != other_attr:
                    return False
        return True

    @property
    def component_name(self) -> str:
        """
        Get the name of the component.

        Returns:
            str: The name of the component.

        Raises:
            KeyError: If the component name is not found in the component.
        """
        if "name" not in dir(self):
            raise KeyError("name not found in component")
        return getattr(self, "name")

    @property
    def component_version(self) -> str:
        """
        Get the version of the dependency.

        Returns:
            str: The version of the dependency.

        Raises:
            KeyError: If the version is not found in the component.
        """
        if "version" not in dir(self):
            raise KeyError("version not found in component")
        return getattr(self, "version")

    @property
    def platform(self) -> str:
        """
        Get the platform of the dependency.

        Returns:
            str: The platform of the dependency.

        Raises:
            KeyError: If the URL is not found in the component external
                      references.
            ValueError: If the URL is not a valid URL.
        """
        return self._get_git_url().split("/", maxsplit=1)[0]

    @property
    def repo_path(self) -> str:
        """
        Get the repo path of the dependency.

        Returns:
            str: The repo path of the dependency.

        Raises:
            KeyError: If the URL is not found in the component external
                      references.
            ValueError: If the URL is not a valid URL.
        """
        return self._get_git_url().split("/", maxsplit=1)[1]

    @property
    def git_url(self) -> str:
        """
        Get the URL of the dependency.

        Returns:
            str: The URL of the dependency.

        Raises:
            KeyError: If the URL is not found in the component external
                      references.
            ValueError: If the URL is not a valid URL.
        """
        git_url = self._get_git_url()
        return f"https://{git_url}"

    def _get_git_url(self) -> str:
        if "externalReferences" not in dir(self):
            raise KeyError("externalReferences not found in component")
        external_ref = getattr(self, "externalReferences")
        urls = []
        for ref in external_ref:
            if "url" not in ref:
                continue
            try:
                github_url = self._parse_github_url(ref["url"])
            except ValueError:
                continue
            urls.append(github_url)
        if not urls:
            raise ValueError("No valid URLs found in externalReferences")
        return urls[0]

    def _parse_github_url(self, url: str) -> str:
        """
        Parse the git URL from a URL.

        Args:
            url (str): The URL to parse.

        Returns:
            str: The git URL.
        """
        url_split = urlparse(url)
        platform = url_split.netloc

        if platform != "github.com":
            raise ValueError("Platform not supported")
        git_repo_path = url_split.path.removesuffix(".git")
        pattern = r"\/([^\/]+)\/([^\/]+)"  # Match /owner/repo
        _match = search(pattern, git_repo_path)
        if not _match:
            raise ValueError("Could not parse git URL")
        git_repo_path = _match.group(0)
        github_url = platform + git_repo_path
        return github_url

    def to_dict(self) -> dict:
        """
        Convert the dependency to a dictionary.

        Returns:
            dict: The dictionary representation of the dependency.
        """
        dependency_dict = {}
        for attr in self.__dict__:
            if attr not in ("dependency_score", "failure_reason"):
                dependency_dict.update({attr: getattr(self, attr)})
            if attr == "dependency_score":
                dependency_dict.update(
                        {"dependency_score":
                         self.dependency_score.to_dict()
                         if self.dependency_score else None
                         }
                )
            if attr == "failure_reason":
                dependency_dict.update(
                        {"failure_reason":
                         str(self.failure_reason)
                         if self.failure_reason else None
                         }
                )

        # Only allow path if it is a valid GitHub URL
        try:
            platform = self.platform
            repo_path = self.repo_path
        except (KeyError, ValueError):
            return dependency_dict

        dependency_dict.update({"platform_path": platform + repo_path})
        return dependency_dict
