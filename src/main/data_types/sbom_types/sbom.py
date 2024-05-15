"""
This module contains the Sbom class, which represents a
Software Bill of Materials (SBOM) object.

Classes:
- Sbom: Represents a Software Bill of Materials (SBOM) object.
"""

from re import match
import requests
from main.data_types.sbom_types.dependency_manager import DependencyManager
from main.data_types.sbom_types.dependency import Dependency
from main.util import get_github_token


class Sbom:
    """
    Represents a Software Bill of Materials (SBOM) object.

    Attributes:
        dependency_manager (DependencyManager): The dependency manager for the
                                                SBOM.
        serial_number (str): The serial number of the SBOM.
        version (str): The version of the SBOM.
        repo_name (str): The name of the repository.
        repo_version (str): The version of the repository.
        spec_version (str): The specification version of the SBOM.
    """
    dependency_manager: DependencyManager
    serial_number: str
    version: int
    repo_name: str
    repo_version: str
    spec_version: str

    def __init__(self, sbom: dict):
        """
        Initializes the SBOM.

        Args:
            sbom (dict): The SBOM contents.
        """
        self._check_format_of_sbom(sbom)
        self.dependency_manager: DependencyManager \
            = DependencyManager(sbom["components"])

        self.serial_number: str = sbom["serialNumber"]
        self.version: int = sbom["version"]
        self.repo_name: str = sbom["metadata"]["component"]["name"]
        self.repo_version: str = sbom["metadata"]["component"]["version"]
        self.spec_version: str = sbom["specVersion"]

    def to_dict(self) -> dict:
        """
        Creates a dictionary representing the SBOM.

        Returns:
            dict: The SBOM as a dictionary.
        """
        res = {}
        res["serialNumber"] = self.serial_number
        res["version"] = self.version
        res["repo_name"] = self.repo_name
        res["repo_version"] = self.repo_version

        # Add dependencies to the dictionary
        dependencies = self.dependency_manager.to_dict()
        for key, value in dependencies.items():
            res[key] = value

        return res

    def to_dict_web(self) -> dict:
        """
        Creates a dictionary representing the SBOM to use in the web
        interface.

        Returns:
            dict: The SBOM as a dictionary.
        """
        res = {}
        res["serialNumber"] = self.serial_number
        res["version"] = self.version
        res["repo_name"] = self.repo_name
        res["repo_version"] = self.repo_version

        # Add dependencies to the dictionary
        dependencies = self.dependency_manager.to_dict_web()
        for key, value in dependencies.items():
            res[key] = value

        return res

    def get_scored_dependencies(self) -> list[Dependency]:
        """
        Gets the scored dependencies of the SBOM.

        Returns:
            list[Dependency]: The scored dependencies of the SBOM.
        """
        return self.dependency_manager.get_scored_dependencies()

    def get_unscored_dependencies(self) -> list[Dependency]:
        """
        Gets the unscored dependencies of the SBOM.

        Returns:
            list[Dependency]: The unscored dependencies of the SBOM.
        """
        return self.dependency_manager.get_unscored_dependencies()

    def get_failed_dependencies(self) -> list[Dependency]:
        """
        Gets the failed dependencies of the SBOM.

        Returns:
            list[Dependency]: The failed dependencies of the SBOM.
        """
        return self.dependency_manager.get_failed_dependencies()

    def get_dependencies_by_filter(self, dependency_filter: callable) \
            -> list[Dependency]:
        """
        Gets the dependencies of the SBOM with a filter.

        Returns:
            list[Dependency]: The filtered dependencies of the SBOM.
        """
        return self.dependency_manager.get_dependencies_by_filter(
            dependency_filter
            )

    def update_dependencies(self, dependencies: list[Dependency]) -> None:
        """
        Updates the dependencies of the SBOM.

        Args:
            dependencies (list[Dependency]): The dependencies to update.
        """
        self.dependency_manager.update(dependencies)

    def _check_format_of_sbom(self, sbom_contents: dict) -> None:
        """
        Checks the format of the SBOM contents.

        Args:
            sbom_contents (dict): The SBOM contents to be checked.

        Raises:
            SyntaxError: If the 'bomFormat' is missing or not 'CycloneDX'.
            IndexError: If the 'specVersion' is missing, out of date, or
                        incorrect.
            SyntaxError: If the 'serialNumber' does not match the RFC-4122
                         format.
            IndexError: If the 'version' of SBOM is lower than 1
            or not a proper integer.
            ValueError: If the name could not be found, indicating a non-valid
                        SBOM.
        """
        if not sbom_contents["bomFormat"] == "CycloneDX":
            raise SyntaxError("bomFormat missing or not CycloneDX")

        if not sbom_contents["specVersion"] in ["1.2", "1.3", "1.4", "1.5"]:
            raise IndexError(
                "CycloneDX version missing, out of date or incorrect"
                )

        if not match(
                "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-" +
                "[0-9a-f]{4}-[0-9a-f]{12}$",
                sbom_contents["serialNumber"]):
            raise SyntaxError(
                "SBOM Serial number does not match the RFC-4122 format")

        if not sbom_contents["version"] >= 1:
            raise IndexError("Version of SBOM is lower than 1")

        if not isinstance(sbom_contents["version"], int):
            raise IndexError("Version of SBOM is not proper integer")

        # Checks if name of SBOM exists
        try:
            name = sbom_contents["metadata"]["component"]["name"]
        except (IndexError, KeyError):
            name = ""

        if name == "":
            raise ValueError("Name could not be found, non valid SBOM")

    def _try_git_api_connection(self, url: str) -> None:
        """
        Tries to connect to the GitHub API.

        Args:
            url (str): The URL to connect to.

        Raises:
            ConnectionError: If the connection could not be established.
        """
        token = get_github_token()
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        url = url.removeprefix("github.com")
        url = f"https://api.github.com/repos{url}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                print(f"Could not connect to {url} {response.text}")
                raise ConnectionError(
                    f"Could not connect to GitHub API for {url}")
        except requests.exceptions.ConnectionError as e:
            raise e
