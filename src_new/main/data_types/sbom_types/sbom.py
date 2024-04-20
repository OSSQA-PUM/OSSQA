"""
This module contains the Sbom class, which represents a
Software Bill of Materials (SBOM) object.

Classes:
- Sbom: Represents a Software Bill of Materials (SBOM) object.
"""

from re import match
from urllib.parse import urlparse
from data_types.sbom_types.dependency_manager import DependencyManager
from data_types.sbom_types.dependency import Dependency
import requests


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
    """
    dependency_manager: DependencyManager
    serial_number: str
    version: str
    repo_name: str
    repo_version: str

    def __init__(self, sbom: dict):
        self._check_format_of_sbom(sbom)
        self.dependency_manager: DependencyManager = DependencyManager()
        self.dependency_manager.update(
            self._parse_components(sbom["components"])
            )

        self.serial_number: str = sbom["serialNumber"]
        self.version: str = sbom["version"]
        self.repo_name: str = sbom["metadata"]["component"]["name"]
        self.repo_version: str = sbom["metadata"]["component"]["version"]

    def to_dict(self) -> dict:
        """
        Converts the SBOM object to a dictionary.

        Returns:
            dict: The SBOM object as a dictionary.
        """
        return {
            "serialNumber": self.serial_number,
            "version": self.version,
            "repo_name": self.repo_name,
            "repo_version": self.repo_version,
            "dependencies": [
                self.dependency_manager.to_dict()
            ]
        }

    def _check_format_of_sbom(self, sbom_file: dict) -> None:
        """
        Checks the format of the SBOM file.

        Args:
            sbom_file (dict): The SBOM file to be checked.

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
        if not sbom_file["bomFormat"] == "CycloneDX":
            raise SyntaxError("bomFormat missing or not CycloneDX")

        if not sbom_file["specVersion"] in ["1.2", "1.3", "1.4", "1.5"]:
            raise IndexError(
                "CycloneDX version missing, out of date or incorrect"
                )

        if not match(
                "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-" +
                "[0-9a-f]{4}-[0-9a-f]{12}$",
                sbom_file["serialNumber"]):
            raise SyntaxError(
                "SBOM Serial number does not match the RFC-4122 format")

        if not sbom_file["version"] >= 1:
            raise IndexError("Version of SBOM is lower than 1")

        if not isinstance(sbom_file["version"], int):
            raise IndexError("Version of SBOM is not proper integer")

        # Checks if name of SBOM exists
        try:
            name = sbom_file["metadata"]["tools"][0]["name"]
        except (IndexError, KeyError):
            name = ""

        if name == "":
            raise ValueError("Name could not be found, non valid SBOM")

    def _parse_components(self, components: list[dict]) -> list[Dependency]:
        """
        Parses a list of component dictionaries.

        Args:
            components (list[dict]): The list of component dictionaries.

        Returns:
            list[Dependency]: A list of parsed Dependency objects.
        """
        dependencies: list[Dependency] = []
        for component in components:
            dependency = self._parse_component(component)
            dependencies.append(dependency)
        return dependencies

    def _parse_component(self, component: dict):
        """
        Parses a component dictionary.

        Args:
            component (dict): The component dictionary.

        Returns:
            Dependency: The parsed Dependency object.
        """
        dependency: Dependency = Dependency()
        try:
            dependency.name = self._parse_git_url(
                self._get_component_url(component=component)
                )
            dependency.version = component["version"]
        except (ConnectionError, KeyError, NameError, ValueError) as e:
            dependency.failure_reason = e
        return dependency

    def _parse_git_url(self, url: str) -> str:
        """
        Parses the git URL and returns the platform,
        repository owner, and repository name.

        Args:
            url (str): The git URL.

        Returns:
            str: The dependency name

        Raises:
            ValueError: If the platform is not supported.
        """
        url_split = urlparse(url)
        platform = url_split.netloc

        if platform != "github.com":
            raise ValueError("Platform not supported")

        name = platform + url_split.path
        return name

    def _get_component_url(self, component: dict) -> str:
        """
        Retrieves the URL of a component from its external references.

        Args:
            component (dict): The component dictionary.

        Returns:
            str: The URL of the component.

        Raises:
            KeyError:
            If no external references are found.

            ConnectionError:
            If there is a connection error while accessing the URL.

            NameError:
            If no VCS (Version Control System) external reference is found.
        """
        external_refs = component.get("externalReferences")
        if not external_refs:
            raise KeyError("No external references found")
        for external_ref in external_refs:
            if external_ref["type"] != "vcs":
                continue

            url = external_ref["url"]
            try:
                response = requests.get(url, timeout=5)
            except (requests.ConnectTimeout, requests.ReadTimeout) as e:
                raise ConnectionError(f"Connection to {url} timed out") from e
            except requests.ConnectionError as e:
                raise ConnectionError(f"Failed to connect to {url}") from e

            if response.status_code != 200:
                raise ConnectionError(f"Failed to connect to {url}")

            response_url = response.url
            return response_url
        raise NameError("No VCS external reference found")