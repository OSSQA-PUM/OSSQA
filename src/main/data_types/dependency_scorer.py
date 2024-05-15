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
from time import sleep
import re
import json
import copy
import os
import requests
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from main.data_types.event import Event
from main.util import (get_git_sha1,
                       get_token_data,
                       Sha1NotFoundError,
                       TokenLimitExceededError)


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

    This class is an abstract base class based on the Strategy design pattern.

    Attributes:
        on_step_complete (Event[StepResponse]): An event that triggers when a
        step in the scoring process is completed.

    Methods:
        score: An abstract function that intends to score a list of
        dependencies.
    """
    on_step_complete: Event[StepResponse]
    _scored_dependencies: list[Dependency]

    def __init__(self, callback: Callable[[StepResponse], Any]) -> None:
        super().__init__()
        self.on_step_complete = Event[StepResponse]()
        self.on_step_complete.subscribe(callback)
        self._scored_dependencies = []

    @abstractmethod
    def score(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        An abstract function that intends to score a list of dependencies.

        Args:
            dependencies (list[Dependency]): The dependencies to score.

        Returns:
            list[Dependency]: The scored dependencies.
        """

    def _check_if_scored(self, dependency: Dependency) -> bool:
        """
        Checks if a dependency has already been scored.
        Also updates the dependency with the score if it has been scored.

        Args:
            dependency (Dependency): The dependency to check.

        Returns:
            bool: True if the dependency has already been scored,
                  False otherwise.
        """
        for scored_dep in self._scored_dependencies:
            if (dependency.git_url == scored_dep.git_url and
                    dependency.component_version ==
                    scored_dep.component_version):
                dependency.scorecard = scored_dep.scorecard
                dependency.failure_reason = scored_dep.failure_reason
                return True
        return False


class SSFAPIFetcher(DependencyScorer):
    """
    Represents a SSF API fetcher.

    This class fetches dependencies with scores from the OpenSSF Scorecard API.

    Attributes:
        on_step_complete (Event[StepResponse]): An event that triggers when a
        step in the scoring process is completed.

    Methods:
        score: Scores a list of dependencies by fetching stored scores with
        the OpenSSF Scorecard API.
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
        remaining_dependencies: list[Dependency] = copy.deepcopy(dependencies)
        try:
            with Pool() as pool:
                for index, dependency in enumerate(
                        pool.imap(self._request_ssf_api, dependencies)
                        ):
                    if dependency.scorecard:
                        successful_items += 1
                    else:
                        failed_items += 1

                    remaining_dependencies.remove(dependency)
                    new_dependencies.append(dependency)
                    self.on_step_complete.invoke(
                        StepResponse(
                            batch_size,
                            successful_items + failed_items,
                            successful_items,
                            failed_items
                        )
                    )
        except TokenLimitExceededError as e:
            time_to_wait: int = e.time_to_wait + 10
            self.on_step_complete.invoke(
                StepResponse(
                    batch_size,
                    successful_items + failed_items,
                    successful_items,
                    failed_items,
                    f"Token limit reached. Until {e.reset_datetime}" +
                    "for token reset."
                )
            )
            sleep(time_to_wait)
            return new_dependencies + self.score(remaining_dependencies)

        return new_dependencies

    def _request_ssf_api(self, dependency: Dependency) -> Dependency:
        """
        Looks up the score for a dependency in the SSF API.

        Args:
            dependency (Dependency): The dependency to look up.

        Returns:
            Dependency: The dependency with an SSF score.

        Raises:
            TokenLimitExceededError: If the GitHub token limit is exceeded.
        """

        assert isinstance(dependency, Dependency), \
            f"dependency: {dependency} is not a Dependency object"

        new_dependency: Dependency = copy.deepcopy(dependency)

        # Check if the dependency has already been scored
        if self._check_if_scored(new_dependency):
            return new_dependency

        try:
            repo_path = new_dependency.repo_path
            component_version = new_dependency.component_version
        except (KeyError, ValueError) as e:
            error_message = f"Failed missing required field due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency

        try:
            sha1 = get_git_sha1(repo_path,
                                component_version)
        except (
                ConnectionRefusedError,
                AssertionError,
                ValueError,
                KeyError,
                Sha1NotFoundError) as e:
            error_message = f"Failed to get git sha1 due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency
        except TokenLimitExceededError as e:
            raise TokenLimitExceededError(e.reset_time) from e

        try:
            score = self._lookup_ssf_api(
                dependency.git_url.lstrip("htps:/"),
                sha1
                )
            new_dependency.scorecard = score
            self._scored_dependencies.append(new_dependency)
            new_dependency.failure_reason = None
            return new_dependency
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to get score due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency

    def _lookup_ssf_api(self, git_url: str, sha1: str) -> Scorecard:
        """
        Looks up the score for a dependency in the SSF API.

        Args:
            git_url (str): The Git URL of the dependency.
            sha1 (str): The SHA1 hash of the dependency.

        Returns:
            Scorecard: The scorecard of the dependency.

        Raises:
            requests.exceptions.RequestException: If the scorecard failed to
            be retrieved.
        """
        try:
            score = requests.get(
                ("https://api.securityscorecards.dev/projects/"
                    f"{git_url}/?commit={sha1}"),
                timeout=10
                )
            if score.status_code != 200:
                score = requests.get(
                    (f"https://api.securityscorecards.dev"
                        f"/projects/{git_url}"),
                    timeout=10
                )
            if score.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"Failed to get score for {git_url} at {sha1}"
                )
            score = score.json()
            return Scorecard(score)
        except requests.exceptions.RequestException as e:
            raise e


class ScorecardAnalyzer(DependencyScorer):
    """
    Represents a Scorecard Analyzer.

    This class scores dependencies by analyzing the scores of the OpenSSF
    Scorecard.

    Attributes:
        on_step_complete (Event[StepResponse]): An event that triggers when a
        step in the scoring process is completed.

    Methods:
        score: Scores a list of dependencies by analyzing the scores of the
        OpenSSF Scorecard.
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
        remaining_dependencies: list[Dependency] = copy.deepcopy(dependencies)

        with Pool() as pool:
            try:
                for index, scored_dependency in enumerate(
                        pool.imap(self._analyze_scorecard, dependencies)
                        ):

                    if scored_dependency.scorecard:
                        successful_items += 1
                    else:
                        failed_items += 1

                    new_dependencies.append(scored_dependency)
                    remaining_dependencies.remove(scored_dependency)
                    self.on_step_complete.invoke(
                        StepResponse(
                            batch_size,
                            index + 1,
                            successful_items,
                            failed_items
                        )
                    )
            except TokenLimitExceededError as e:
                time_to_wait: int = e.time_to_wait + 10
                self.on_step_complete.invoke(
                    StepResponse(
                        batch_size,
                        successful_items + failed_items,
                        successful_items,
                        failed_items,
                        "Token limit reached. Waiting until " +
                        f"{e.reset_datetime} for token reset."
                    )
                )
                sleep(time_to_wait)
                return new_dependencies + self.score(remaining_dependencies)

        return new_dependencies

    def _analyze_scorecard(self, dependency: Dependency, timeout: float = 120)\
            -> Dependency:
        """
        Analyzes the score for a dependency.

        Args:
            dependency (Dependency): The dependency to analyze.
            timeout (float): Time for requests to timeout

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
            TimeoutError: If the scorecard execution timed out.
            TokenLimitExceededError: If the GitHub token limit is exceeded.
        """
        assert isinstance(dependency, Dependency), \
            f"dependency: {dependency} is not a Dependency object"

        new_dependency: Dependency = copy.deepcopy(dependency)

        # Check if the dependency has already been scored
        if self._check_if_scored(new_dependency):
            return new_dependency

        try:
            repo_path = new_dependency.repo_path
            component_version = new_dependency.component_version
        except (KeyError, ValueError) as e:
            error_message = f"Failed missing required field due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency

        try:
            version_git_sha1: str = get_git_sha1(
                repo_path, component_version
            )
        except (
                ConnectionRefusedError,
                AssertionError,
                ValueError,
                KeyError,
                Sha1NotFoundError) as e:
            error_message = f"Failed to get git sha1 due to: {e}"
            new_dependency.failure_reason = type(e)(error_message)
            return new_dependency
        except TokenLimitExceededError as e:
            raise TokenLimitExceededError(e.reset_time) from e

        remaining_tries: int = 3
        retry_interval: int = 3
        success: bool = False
        while remaining_tries > 0 and not success:
            try:
                remaining_tries -= 1
                scorecard: Scorecard = self._execute_scorecard(
                    new_dependency.git_url, version_git_sha1, timeout
                    )

                new_dependency.scorecard = scorecard
                self._scored_dependencies.append(new_dependency)

                success = True
            except (AssertionError,
                    subprocess.CalledProcessError,
                    TimeoutError,
                    json.JSONDecodeError,
                    ValueError,
                    requests.ConnectionError) as e:
                error_message = f"Failed to execute scorecard due to: {e}"
                new_dependency.failure_reason = type(e)(error_message)
                sleep(retry_interval)  # Wait before retrying
                continue
            except TokenLimitExceededError as e:
                raise TokenLimitExceededError(e.reset_time) from e

        # Successful execution of scorecard
        if new_dependency.scorecard:
            new_dependency.failure_reason = None
        return new_dependency

    def _execute_scorecard(self,
                           git_url: str,
                           commit_sha1: str,
                           timeout: float = 120) -> Scorecard:
        """
        Executes the OpenSSF Scorecard binary
        on a specific version of a dependency.

        Args:
            git_url (str): The Git URL of the dependency.
            version (str): The version of the dependency.
            timeout (float): The timeout in seconds for the scorecard binary.

        Returns:
            Scorecard: The scorecard of the dependency.

        Raises:
            AssertionError: If the git url is not a string.
            AssertionError: If the commit sha1 is not a string.
            ValueError: If the scorecard output could not be parsed.
            json.JSONDecodeError: If the scorecard output could not be parsed.
            subprocess.CalledProcessError: If the scorecard binary could not be
                                             executed.
            TimeoutError: If the scorecard execution timed out.
        """
        # Validate input
        assert isinstance(git_url, str), f"git_url: {git_url} is not a string"
        assert isinstance(commit_sha1, str), \
            f"commit_sha1: {commit_sha1} is not a string."

        # Set flags for scorecard binary
        flags: str = (f"--repo {git_url} --show-details "
                      f"--format json --commit {commit_sha1}")
        # Execute scorecard binary and get the raw output as a string
        try:
            # Execute scorecard binary if OS is Windows or Unix
            if os.name == "nt":
                output: str = subprocess.check_output(
                    f'scorecard-windows.exe {flags}',
                    shell=False,
                    timeout=timeout
                ).decode("utf-8")
            else:
                output: str = subprocess.check_output(
                    f'scorecard {flags}',
                    shell=True,
                    timeout=timeout
                ).decode("utf-8")
        except (subprocess.CalledProcessError) as e:
            output = e.output.decode("utf-8")
        except subprocess.TimeoutExpired as e:
            token_data: dict = get_token_data()
            if token_data.get("remaining") == 0:
                raise TokenLimitExceededError(
                    token_data.get("reset_time"))
            raise TimeoutError(e.timeout,
                               "Scorecard execution timed out") from e

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
