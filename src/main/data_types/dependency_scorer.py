"""
This module contains classes for analyzing or fetching dependencies.

The class DependencyScorer is an abstract base class based on the 
Strategy design pattern, with children implementing different ways
of retrieving Dependencies with scored data.
"""
from abc import ABC, abstractmethod
from typing import Any, Callable
from dataclasses import dataclass
import subprocess
from multiprocessing import Pool
import re
import json
import copy
import os
from time import sleep
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from main.data_types.event import Event
from main.util import get_git_sha1


@dataclass
class StepResponse:
    """
    Represents a response from a step in the dependency scoring process.
    """
    batch_size: int
    completed_items: int
    successful_items: int
    failed_items: int
    message: str = ""


class DependencyScorer(ABC):
    """
    Represents a dependency scorer.
    """
    on_step_complete: Event[StepResponse]

    def __init__(self, callback: Callable[[StepResponse], Any]) -> None:
        super().__init__()
        self.on_step_complete = Event[StepResponse]()
        self.on_step_complete.subscribe(callback)

    @abstractmethod
    def score(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        An abstract function that intends to score a list of dependencies.

        Args:
            dependencies (list[Dependency]): The dependencies to score.

        Returns:
            list[Dependency]: The scored dependencies.
        """


class SSFAPIFetcher(DependencyScorer):
    """
    Represents a SSF API fetcher
    """
    def score(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        Scores a list of dependencies by fetching stored scores with
        the OpenSSF Scorecard API.

        Args:
            dependencies (list[Dependency]): The dependencies to score.

        Returns:
            list[Dependency]: The scored dependencies.
        """
        batch_size = len(dependencies)
        failed_items = 0
        successful_items = 0
        new_dependencies = []

        for index, dependency in enumerate(dependencies):
            # Process dependency
            new_dependency = self._request_ssf_api(dependency)
            new_dependencies.append(new_dependency)
            self.on_step_complete.invoke(
                StepResponse(
                    batch_size, index + 1,
                    successful_items,
                    failed_items
                    )
                )

        return new_dependencies

    def _request_ssf_api(self, dependency: Dependency) -> Dependency:
        """
        Looks up the score for a dependency in the SSF API.

        Args:
            dependency (Dependency): The dependency to look up.

        Returns:
            Dependency: The dependency with an SSF score.
        """
        # TODO
        # 1. Get commit sha1 of the dependency's version
        # 2. Request the score from the SSF API
        # 3. If the request is successful construct a new Dependency object
        # 4. Else return a copy of the old dependency
        new_dependency = Dependency()
        return new_dependency


class ScorecardAnalyzer(DependencyScorer):
    """
    Represents a scorecard analyzer
    """
    def score(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        Scores a list of dependencies by analyzing the scores of the
        OpenSSF Scorecard.

        Args:
            dependencies (list[Dependency]): The dependencies to score.

        Returns:
            list[Dependency]: The scored dependencies.

        Raises:
            AssertionError: If the dependencies is not a list.
        """
        assert isinstance(dependencies, list), \
            f"dependencies: {dependencies} is not a list"
        batch_size = len(dependencies)
        failed_items = 0
        successful_items = 0
        new_dependencies = []

        with Pool() as pool:
            for index, scored_dependency in enumerate(
                    pool.imap(self._analyze_scorecard, dependencies)
                    ):

                if scored_dependency.dependency_score:
                    successful_items += 1
                else:
                    failed_items += 1

                new_dependencies.append(scored_dependency)
                self.on_step_complete.invoke(
                    StepResponse(
                        batch_size,
                        index + 1,
                        successful_items,
                        failed_items
                    )
                )

        return new_dependencies

    def _analyze_scorecard(self, dependency: Dependency) -> Dependency:
        """
        Analyzes the score for a dependency.

        Args:
            dependency (Dependency): The dependency to analyze.

        Returns:
            Dependency: A deepcopy the dependency with an analyzed score.

        Raises:
            AssertionError: If the git sha1 is invalid.
            AssertionError: If the dependency is not a Dependency object.
            AssertionError: If the scorecard could not be executed.
            ConnectionRefusedError: If the git sha1 could not be retrieved.
            subprocess.CalledProcessError: If the scorecard binary could not be
                                           executed.
            json.JSONDecodeError: If the scorecard output could not be parsed.
        """
        assert isinstance(dependency, Dependency), \
            f"dependency: {dependency} is not a Dependency object"

        new_dependency: Dependency = copy.deepcopy(dependency)
        try:
            version_git_sha1: str = get_git_sha1(
                self, new_dependency.url, new_dependency.version
            )
        except (ConnectionRefusedError, AssertionError) as e:
            error_message = f"Failed to get git sha1 due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency

        remaining_tries: int = 3
        retry_interval: int = 3
        success: bool = False

        while remaining_tries > 0 and not success:
            try:
                remaining_tries -= 1
                scorecard: Scorecard = self._execute_scorecard(
                    new_dependency.url, version_git_sha1
                    )
                new_dependency.dependency_score = scorecard
                success = True
            except (AssertionError,
                    subprocess.CalledProcessError,
                    json.JSONDecodeError) as e:
                error_message = f"Failed to execute scorecard due to: {e}"
                new_dependency.failure_reason = type(e)(error_message)
                sleep(retry_interval)
                continue

        return new_dependency

    def _execute_scorecard(self,
                           git_url: str,
                           commit_sha1: str,
                           timeout: int = 120) -> Scorecard:
        """
        Executes the OpenSSF Scorecard binary
        on a specific version of a dependency.

        Args:
            git_url (str): The Git URL of the dependency.
            version (str): The version of the dependency.
            timeout (int): The timeout in seconds for the scorecard binary.

        Returns:
            Scorecard: The scorecard of the dependency.

        Raises:
            AssertionError: If the git url is not a string.
            AssertionError: If the commit sha1 is not a string.
            ValueError: If the scorecard output could not be parsed.
            subprocess.CalledProcessError: If the scorecard binary could not be
                                           executed.
            json.JSONDecodeError: If the scorecard output could not be parsed.
        """
        # Validate input
        assert isinstance(git_url, str), f"git_url: {git_url} is not a string"
        assert isinstance(commit_sha1, str), \
            f"commit_sha1: {commit_sha1} is not a string."

        # Set flags for scorecard binary
        flags: str = (f"--repo {git_url} --show-details "
                      f"--format json --commit {commit_sha1}")
        print(f"Executing scorecard for {git_url} at {commit_sha1}")
        # Execute scorecard binary and get the raw output as a string
        try:
            # Execute scorecard binary if OS is Windows or Unix
            if os.name == "nt":
                output: str = subprocess.check_output(
                    f'scorecard-windows.exe {flags}',
                    shell=True,
                    timeout=timeout
                ).decode("utf-8")
            else:
                output: str = subprocess.check_output(
                    f'scorecard {flags}',
                    shell=True,
                    timeout=timeout
                ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            output = e.output.decode("utf-8")
        print(f"Scorecard output: {output}")
        # Remove unnecessary data
        # Find start of JSON used for creating a Scorecard by finding the first
        # '{"date":'
        try:
            start_of_json: int = output.find('{"date":')
            assert start_of_json != -1, "JSON start not found"

            # Find end of JSON by finding the first '}' after the metadata
            pos_of_metadata: int = output.find('"metadata":')
            assert pos_of_metadata != -1, "Metadata not found"
            end_of_json: int = pos_of_metadata + \
                output[pos_of_metadata:].find('}')
            assert end_of_json != -1, "JSON end not found"

            # Remove newlines and save the JSON
            output: str = re.sub(
                r"\n", "",
                output[start_of_json:end_of_json + 1]
            )
            assert output != "", "JSON is empty"
        except AssertionError as e:
            raise ValueError(
                    f"Failed to parse scorecard executable output because {e}"
                ) from e

        # Parse output to dict
        try:
            scorecard_dict: dict = json.loads(output)
            assert scorecard_dict["checks"], "Scorecard checks are empty"
        except json.JSONDecodeError as e:
            raise e

        # Create Scorecard object
        try:
            scorecard: Scorecard = Scorecard(scorecard_dict)
        except AssertionError as e:
            raise AssertionError(
                    "Failed to create Scorecard object from dict: " +
                    f"{scorecard_dict} because {e}"
                ) from e
        return scorecard


def test():
    analyser = ScorecardAnalyzer(lambda x: None)
    analyser._execute_scorecard(
        "github.com/pytorch/pytorch",
        "63397ac3f9402e05f1795f35bb381c236dadd1d4")