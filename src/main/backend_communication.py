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
from main.data_types.sbom_types.scorecard import Scorecard
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.dependency_scorer import DependencyScorer, StepResponse
from main.data_types.event import Event
from main.constants import HOST


class BackendCommunication:
    """
    Represents backend communication.
    Can add SBOMs to the database and get SBOMs from the database.
    Will also inform user about the status of the operation.
    """
    on_status_changed: Event[StepResponse]
    backend_fetcher: DependencyScorer

    def __init__(self, callback: Callable[[StepResponse], Any]) -> None:
        self.on_status_changed = Event[StepResponse]()
        self.on_status_changed.subscribe(callback)
        self.backend_fetcher = BackendFetcher(callback)

    async def add_sbom(self, sbom: Sbom) -> None:
        """
        Adds an SBOM, its dependencies, and their scores to the database.

        Args:
            sbom (Sbom): The SBOM to add to the database.
        """
        try:
            requests.post(HOST + "/sbom", json=sbom.to_dict(), timeout=5)
        except requests.exceptions.Timeout:
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
            response = requests.get(HOST + f"/sbom/{name}", timeout=5)
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
                )

        result: list[Sbom] = []
        if response.status_code != 200:
            return result

        for sbom in response.json():
            sbom_obj = Sbom(sbom=sbom)
            result.append(sbom_obj)

        return result

    def get_sbom_names(self) -> list[str]:
        """
        Returns the names of all the SBOMs in the database.

        Returns:
            list[str]: A list containing the names of all SBOM:s
        """
        try:
            response = requests.get(HOST + "/sbom", timeout=5)
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_status_changed.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
                )
        return response.json() if response.status_code == 200 else []


class BackendFetcher(DependencyScorer):
    """
    Represents a backend fetcher
    """
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
        dependency_primary_keys = []
        for dependency in dependencies:
            dependency_primary_keys.append({
                dependency.name,
                dependency.version,
            })

        try:
            response = requests.get(HOST + "/get_existing_dependencies",
                                    json=dependency_primary_keys,
                                    timeout=5
                                    )
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_step_complete.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
                )
            return []
        except TypeError:
            # Tell the user that the response was not JSON
            self.on_step_complete.invoke(
                StepResponse(0, 0, 0, 0, "The response was not JSON")
                )
            return []

        result: list[Dependency] = []
        if not response or response.status_code != 200:
            return result

        for dependency in response.json():
            name = dependency["name"]
            version = dependency["version"]
            scorecard = Scorecard(dependency["score"])

            dep_obj = Dependency(name=name,
                                 version=version,
                                 dependency_score=scorecard
                                 )
            result.append(dep_obj)
        return result
