"""
This module contains functions for communicating with the database.

Functions:
- add_sbom: Adds an SBOM, its dependencies, and their scores to the database.
- get_sboms_by_name: Gets all versions of a SBOM:s with a specific name.
- get_sbom_names: Returns the names of all the SBOMs in the database.
- get_existing_dependencies: Gets saved dependencies from the database.
"""
from typing import Any, Callable
import copy
import requests
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.dependency_scorer import DependencyScorer, StepResponse
from main.data_types.event import Event
from main.util import get_git_sha1



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
    def __init__(self, callback: Callable[[StepResponse], Any], host: str) -> None:
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
        new_dependencies = self._get_existing_scorecards(dependencies)
        step_response: StepResponse = StepResponse(
            len(dependencies), len(dependencies),
            len(new_dependencies), len(dependencies) - len(new_dependencies)
        )
        self.on_step_complete.invoke(step_response)
        return new_dependencies

    def _get_existing_scorecards(self, dependencies: list[Dependency]) \
            -> list[Dependency]:
        """
        Gets saved scorecards from the database

        Args:
        dependencies (list[Dependency]): The dependencies to check

        Returns:
            list[Dependency]: The dependencies with added scorecards
                              from the database
        """
        scorecard_primary_key = {"repo":
                                 {"name": "",
                                  "commmit": ""}}
        new_dependencies: list[Dependency] = []
        commit_map = {}
        for dependency in dependencies:
            new_dependency = copy.deepcopy(dependency)
            try:
                git_url = dependency.git_url
            except (ValueError, KeyError) as e:
                new_dependency.failure_reason = e
                new_dependencies.append(new_dependency)
                continue
            try:
                commit = get_git_sha1(
                    new_dependency.git_url, new_dependency.component_version
                    )
                commit_map.update({commit: new_dependency})
            except (ValueError, AssertionError, ConnectionRefusedError) as e:
                new_dependency.failure_reason = e
                new_dependencies.append(new_dependency)
                continue

            scorecard_primary_key["repo"]["name"] = git_url
            scorecard_primary_key["repo"]["commit"] = commit
            new_dependencies.append(new_dependency)

        try:
            response = requests.get(self.host + "/scorecard/existing",
                                    json=scorecard_primary_key,
                                    timeout=5
                                    )
        except requests.exceptions.Timeout:
            # Tell the user that the request timed out
            self.on_step_complete.invoke(
                StepResponse(0, 0, 0, 0, "The request timed out")
                )
            return new_dependencies
        except TypeError:
            # Tell the user that the response was not JSON
            self.on_step_complete.invoke(
                StepResponse(0, 0, 0, 0, "The response was not JSON")
                )
            return new_dependencies
        except requests.exceptions.ConnectionError as e:
            # Tell the user that the connection was refused
            self.on_step_complete.invoke(
                StepResponse(0, 0, 0, 0, str(e))
                )
            return new_dependencies
        if not response or response.status_code != 200:
            return new_dependencies

        for scorecard in response.json():
            commit = scorecard["repo"]["commit"]
            dependency: Dependency = commit_map[commit]
            dependency.dependency_score = Scorecard(scorecard)
        return new_dependencies
