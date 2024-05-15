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
        scorecard (Scorecard): The scorecard related to the dependency.
        failure_reason (Exception): The reason for any failure
                                    related to the dependency.
        reach_requirement (str): The grade of the dependency.
    """

    scorecard: Scorecard = None
    failure_reason: Exception = None
    reach_requirement: str = None

    def __init__(self, dependency: dict):
        """
        Initializes the dependency.

        Args:
            dependency (dict): The component counterpart of the dependency in
            the SBOM.
        """
        self.scorecard = None
        self.failure_reason = None
        self.reach_requirement = None
        for dependency_attr in dependency.keys():
            if dependency_attr == "scorecard":
                self.scorecard = Scorecard(dependency[dependency_attr])
            else:
                setattr(self, dependency_attr, dependency[dependency_attr])

    def __eq__(self, other):
        """
        Check if two dependencies are equal.

        Args:
            other (Dependency): The dependency to compare with.

        Returns:
            bool: True if the dependencies are equal, False otherwise.
        """
        # Loop over all attributes of the dependency
        for attr in self.__dict__:
            if attr not in ("name", "version"):
                continue

            # If the attribute is not the same in both dependencies
            try:
                other_attr = getattr(other, attr)
            except AttributeError:
                return False
            if getattr(self, attr) != other_attr:
                return False
        return True

    @property
    def component(self) -> dict:
        """
        Get all the attributes from the SBOM of the dependency.

        Returns:
            dict: The attributes from the SBOM of the dependency.
        """
        res = {}
        for attr in self.__dict__:
            if attr not in (
                    "scorecard", "failure_reason", "reach_requirement"):
                res.update({attr: getattr(self, attr)})
        return res

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
        Get the version of the component.

        Returns:
            str: The version of the component.

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
        Get the git URL of the dependency.

        Returns:
            str: The git URL of the dependency.

        Raises:
            ValueError: If no git URL could be found in externalReferences
                        of the component.
            KeyError: If the component has no externalReferences field.
        """
        git_url = self._get_git_url()
        return f"https://{git_url}"

    def _get_git_url(self) -> str:
        """
        Get the git URL of the dependency.

        Returns:
            str: The git URL of the dependency.

        Raises:
            ValueError: If no git URL could be found in externalReferences
                        of the component.
            KeyError: If the component has no externalReferences field.
        """
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
        Parse the GitHub URL from a URL.

        Args:
            url (str): The URL to parse.

        Returns:
            str: The GitHub URL.

        Raises:
            ValueError: If the URL is not a github.com URL or if the URL could
                        not be parsed.
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
        Create a dictionary representing the dependency.

        Returns:
            dict: The dependency as a dictionary.
        """
        dependency_dict = {}
        for attr in self.__dict__:
            if attr not in ("scorecard", "failure_reason"):
                dependency_dict.update({attr: getattr(self, attr)})
            if attr == "scorecard":
                dependency_dict.update(
                        {"scorecard":
                         self.scorecard.to_dict()
                         if self.scorecard else None
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

    def to_dict_web(self) -> dict:
        """
        Creates a dictionary representing the dependency to use in the web
        interface.

        Returns:
            dict: The dependency as a dictionary.
        """
        res = {}
        res["dependency_score"] = self.scorecard.to_dict() \
            if self.scorecard else None
        res["failure_reason"] = str(self.failure_reason) \
            if self.failure_reason else ""
        res["reach_requirement"] = self.reach_requirement
        try:
            platform = self.platform
            repo_path = self.repo_path
            res["name"] = f"{platform}/{repo_path}"
        except (KeyError, ValueError):
            res["name"] = ""
        res["version"] = self.component_version
        return res
