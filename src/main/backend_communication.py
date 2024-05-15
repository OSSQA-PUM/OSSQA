"""
This module contains functions for communicating with the database.

Functions:
- add_sbom: Adds an SBOM, its dependencies, and their scores to the database.
- get_sboms_by_name: Gets all versions of a SBOM:s with a specific name.
- get_sbom_names: Returns the names of all the SBOMs in the database.
- get_existing_dependencies: Gets saved dependencies from the database.
"""
from typing import Any, Callable
import requests
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.dependency_scorer import DependencyScorer, StepResponse
from main.data_types.event import Event


class BackendCommunication:
    """
    Represents backend communication.
    Can add SBOMs to the database and get SBOMs from the database.
    Will also inform user about the status of the operation.
    """
    on_status_changed: Event[StepResponse]
    backend_fetcher: DependencyScorer

    def __init__(self, callback: Callable[[StepResponse], Any], host: str) \
            -> None:
        self.on_status_changed = Event[StepResponse]()
        self.on_status_changed.subscribe(callback)
        self.backend_fetcher = BackendFetcher(callback, host)
        self.host = host.rstrip("/")

    def add_sbom(self, sbom: Sbom) -> None:
        """
        Adds an SBOM, its dependencies, and their scores to the database.

        Args:
            sbom (Sbom): The SBOM to add to the database.
        """
        try:
            resp = requests.post(
                self.host + "/sbom", json=sbom.to_dict(), timeout=5
            )
            if resp.status_code == 500:
                self.on_status_changed.invoke(
                    StepResponse(0, 0, 0, 0, "The sbom could not be uploaded")
                )
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            # Tell the user that the request timed out
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
            )

    def get_sboms_by_name(self, name: str) -> list[Sbom]:
        """
        Gets all versions of a SBOM:s with a specific name.

        Args:
            name (str): The name of the SBOM:s.

        Returns:
            list[Sbom]: A list containing the SBOM:s.
        """
        try:
            response = requests.get(self.host + f"/sbom/{name}", timeout=5)
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
            )

        result: list[Sbom] = []
        if response.status_code != 200:
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "An error occurred in the database")
            )
            return result

        for sbom in response.json():
            print("before")
            sbom_obj = Sbom(sbom=sbom)
            print("after")
            result.append(sbom_obj)

        return result

    def get_sbom_names(self) -> list[str]:
        """
        Returns the names of all the SBOMs in the database.

        Returns:
            list[str]: A list containing the names of all SBOM:s
        """
        try:
            response = requests.get(self.host + "/sbom", timeout=5)
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
            )

        if response.status_code != 200:
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "An error occurred in the database")
            )
            return []

        return response.json()


class BackendFetcher(DependencyScorer):
    """
    Represents a backend fetcher
    """
    def __init__(self, callback: Callable[[StepResponse], Any], host: str) \
            -> None:
        super().__init__(callback)
        self.host = host.rstrip("/")

    def score(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        Scores a list of dependencies by fetching the scores from the backend.

        Args:
            dependencies (list[Dependency]): The dependencies to score.

        Returns:
            list[Dependency]: The scored dependencies.
        """
        new_dependencies = self._get_existing_dependencies(dependencies)
        step_response: StepResponse = StepResponse(
            len(dependencies), len(dependencies),
            len(new_dependencies), len(dependencies) - len(new_dependencies)
        )
        self.on_step_complete.invoke(step_response)
        return new_dependencies

    def _get_existing_dependencies(self, dependencies: list[Dependency]) \
            -> list[Dependency]:
        """
        Gets saved dependencies from the database

        Args:
        dependencies (list[Dependency]): The dependencies to check

        Returns:
            list[Dependency]: The existing dependencies in the database
        """
        batch_size = len(dependencies)
        failed_count = 0
        dep_dicts = []
        for dependency in dependencies:
            try:
                dep_dict = dependency.to_dict()
            except (KeyError, ValueError):
                failed_count += 1
                continue
            dep_dicts.append(dep_dict)

        try:
            response = requests.get(self.host + "/dependency/existing",
                                    json=dep_dicts,
                                    timeout=5
                                    )
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_step_complete.invoke(
                StepResponse(
                    batch_size, 0, 0, failed_count, "The request timed out")
                )
            return []
        except TypeError:
            # Tell the user that the response was not JSON
            self.on_step_complete.invoke(
                StepResponse(
                    batch_size, 0, 0, failed_count,
                    "The response was not JSON")
                )
            return []
        except requests.exceptions.ConnectionError as e:
            # Tell the user that the connection was refused
            self.on_step_complete.invoke(
                StepResponse(batch_size, 0, 0, failed_count, str(e))
                )
            return []

        new_dependencies = []
        if not response or response.status_code != 200:
            return new_dependencies

        for dependency_component in response.json():
            dep_obj = Dependency(dependency_component)
            new_dependencies.append(dep_obj)
        return new_dependencies
