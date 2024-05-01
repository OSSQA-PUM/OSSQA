"""
This module contains the Sbom class, which represents a
Software Bill of Materials (SBOM) object.

Classes:
- Sbom: Represents a Software Bill of Materials (SBOM) object.
"""

from re import match, search
from urllib.parse import urlparse
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
    """
    dependency_manager: DependencyManager
    serial_number: str
    version: int
    repo_name: str
    repo_version: str

    def __init__(self, sbom: dict):
        self._check_format_of_sbom(sbom)

        self.dependency_manager: DependencyManager = DependencyManager()
        self.dependency_manager.update(
            self._parse_components(sbom["components"])
            )

        self.serial_number: str = sbom["serialNumber"]
        self.version: int = sbom["version"]
        self.repo_name: str = sbom["metadata"]["component"]["name"]
        self.repo_version: str = sbom["metadata"]["component"]["version"]

    def to_dict(self) -> dict:
        """
        Converts the SBOM object to a dictionary.

        Returns:
            dict: The SBOM object as a dictionary.
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

    def get_scored_dependencies(self) -> list[Dependency]:
        """
        Gets the dependencies of the SBOM.

        Returns:
            list[Dependency]: The dependencies of the SBOM.
        """
        return self.dependency_manager.get_scored_dependencies()

    def get_unscored_dependencies(self) -> list[Dependency]:
        """
        Gets the dependencies of the SBOM.

        Returns:
            list[Dependency]: The dependencies of the SBOM.
        """
        return self.dependency_manager.get_unscored_dependencies()

    def get_failed_dependencies(self) -> list[Dependency]:
        """
        Gets the dependencies of the SBOM.

        Returns:
            list[Dependency]: The dependencies of the SBOM.
        """
        return self.dependency_manager.get_failed_dependencies()

    def get_dependencies_by_filter(self, dependency_filter: callable) \
            -> list[Dependency]:
        """
        Gets the dependencies of the SBOM.

        Returns:
            list[Dependency]: The dependencies of the SBOM.
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
            name = sbom_file["metadata"]["component"]["name"]
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
        dependencies: list[tuple] = []
        for component in components:
            # 1. Parse the component. Get name and version
            try:
                url = self._parse_component_name(component)
            except (KeyError, ValueError) as e:
                print(f"Could not find name in component {component} with "
                      f"error {e}")
                continue
            version = component.get("version")
            name = component.get("name")

            if url is None or version is None or name is None:
                continue

            # 2. Check if the dependency is a duplicate
            if self._is_duplicate(url, version, dependencies):
                continue
            if not url.startswith("github.com"):
                continue

            # Takes a long time to request data for all dependencies
            lookup_path_on_github = False
            if lookup_path_on_github:
                try:
                    self._try_git_api_connection(url)
                except ConnectionError as e:
                    print(f"Could not connect to {url} with error {e}")
                    continue

            dependencies.append((name, url, version))

        # Create dependency object for each component
        new_dependencies = []
        for dependency in dependencies:
            dependency = Dependency(
                name=dependency[0],
                git_url=dependency[1],
                version=dependency[2])
            new_dependencies.append(dependency)
        return new_dependencies

    def _is_duplicate(
            self, name: str, version: str, dependencies: list[tuple]
            ) -> bool:
        """
        Checks if a dependency is a duplicate.

        Args:
            name (str): The name of the dependency.
            version (str): The version of the dependency.
            dependencies (list[tuple]): The list of dependencies.

        Returns:
            bool: True if the dependency is a duplicate, False otherwise.
        """
        for dependency in dependencies:
            if name == dependency[0] and version == dependency[1]:
                return True
        return False

    def _parse_component_name(self, component: dict) -> str:
        """
        Parses the name of a component from a component dictionary.

        Args:
            component (dict): The component dictionary.

        Returns:
            str: The name of the component.
        """
        failure_reason = None
        name = ""
        version = ""
        try:
            # TODO: The name of the component is not in the url.
            #       According to the CycloneDX documentation,
            #       each component has a name that can be accessed via
            #       component["name"].
            #       This should be fixed, preferably by storing the
            #       URL in it's own variable in Dependency, so
            #       that OSSQA adheres to the CycloneDX format,
            #       which in turn makes the behavior of the program
            #       more predictable.
            name = self._parse_git_url(
                self._get_component_url(component=component)
                )
            version = component["version"]
        except (ConnectionError, KeyError, NameError, ValueError) as e:
            failure_reason = e
        dependency = Dependency(name=name, component_name=component["name"], version=version)
        if failure_reason:
            dependency.failure_reason = failure_reason
        return dependency

    def _parse_github_url(self, url: str) -> str:
        """
        Parses the git URL and returns the platform,
        repository owner, and repository name.

        Args:
            url (str): The git URL.

        Returns:
            str: The dependency name

        Raises:
            ValueError: If the platform is not supported.
            ConnectionError: If the connection could not be established.
        """
        url_split = urlparse(url)
        platform = url_split.netloc

        if platform != "github.com":
            raise ValueError("Platform not supported")
        git_repo_path = url_split.path.removesuffix(".git")
        pattern = r"\/([^\/]+)\/([^\/]+)"  # Match /owner/repo
        _match = search(pattern, git_repo_path)
        if _match:
            git_repo_path = _match.group(0)
        github_url = platform + git_repo_path
        return github_url

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
