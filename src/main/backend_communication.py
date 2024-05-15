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

    Attributes:
        on_status_changed (Event[StepResponse]): The event for status changes.
        backend_fetcher (DependencyScorer): The backend fetcher.

    Args:
        callback (Callable[[StepResponse], Any]): The callback function.
        host (str): The host of the backend.
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
        """
        Initializes the backend fetcher.

        Args:
            callback (Callable[[StepResponse], Any]): The callback function.
            host (str): The host of the backend.
        """
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
        success_count = 0
        dep_dicts = []

        current_step = StepResponse(
            batch_size, 0, 0, 0, "Fetching existing dependencies")
        self.on_step_complete.invoke(current_step)

        for dependency in dependencies:
            try:
                dep_dict = dependency.to_dict()
            except (KeyError, ValueError):
                failed_count += 1
                current_step = StepResponse(
                    batch_size, len(dep_dicts) + failed_count,
                    success_count, failed_count,
                    "Failed to convert dependency to dictionary")
                self.on_step_complete.invoke(current_step)
                continue
            dep_dicts.append(dep_dict)

        failure_message: str = ""
        try:
            response = requests.get(self.host + "/dependency/existing",
                                    json=dep_dicts,
                                    timeout=5
                                    )
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            failure_message = "The request timed out"
        except TypeError:
            # Tell the user that the response was not JSON
            failure_message = "The response was not JSON"
        except requests.exceptions.ConnectionError:
            # Tell the user that the connection was refused
            failure_message = "The connection was refused"

        new_dependencies = []
        if failure_message:
            failed_count = batch_size
            current_step = StepResponse(
                batch_size, batch_size,
                success_count, failed_count,
                failure_message)
            self.on_step_complete.invoke(current_step)
            return new_dependencies

        if not response or response.status_code != 200:
            failed_count = batch_size
            current_step = StepResponse(
                batch_size, batch_size,
                success_count, failed_count,
                "Failed to fetch existing dependencies")
            self.on_step_complete.invoke(current_step)
            return new_dependencies

        if not response.json():
            failed_count = batch_size
            current_step = StepResponse(
                batch_size, batch_size,
                success_count, failed_count,
                "No existing dependencies found")
            self.on_step_complete.invoke(current_step)
            return new_dependencies

        failed_count = batch_size - len(response.json())

        for dependency_component in response.json():
            dep_obj = Dependency(dependency_component)
            new_dependencies.append(dep_obj)
            success_count += 1
            current_step = StepResponse(
                batch_size, success_count + failed_count,
                success_count, failed_count,
                "Found existing dependency")
            self.on_step_complete.invoke(current_step)

        return new_dependencies
