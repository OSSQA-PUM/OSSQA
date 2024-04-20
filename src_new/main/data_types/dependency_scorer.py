"""
This module contains functions for analyzing dependencies.

Functions:
- lookup_ssf_api: Looks up the scores for multiple dependencies in the SSF API.
- analyze: Analyzes the scores for multiple dependencies.
"""
from abc import ABC, abstractmethod
from typing import Any, Callable
from dataclasses import dataclass
from data_types.sbom_types.dependency import Dependency
from data_types.sbom_types.scorecard import Scorecard
from data_types.event import Event


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
        """
        new_dependencies = []
        return new_dependencies

    def _analyze_scorecard(self, dependency: Dependency) -> Dependency:
        """
        Analyzes the score for a dependency.

        Args:
            dependency (Dependency): The dependency to analyze.

        Returns:
            Dependency: The dependency with an analyzed score.
        """
        # TODO
        # get git sha1
        # execute scorecard on correct version
        # create new dependency with scorecard
        new_dependency = Dependency()
        return new_dependency

    def _execute_scorecard(self, git_url: str, version: str) -> Scorecard:
        """
        Executes the OpenSSF Scorecard binary
        on a specific version of a dependency.

        Args:
            git_url (str): The Git URL of the dependency.
            version (str): The version of the dependency.

        Returns:
            Scorecard: The scorecard of the dependency.
        """
        # TODO
        # execute scorecard
        # process output (remove unnecessary data)
        # parse output to dict
        # create Scorecard object
        dummy_dict = {}
        scorecard = Scorecard(dummy_dict)
        return scorecard
