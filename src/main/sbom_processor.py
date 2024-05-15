"""
This module contains the SBOM processor class, which is responsible for
processing SBOMs.

Classes:
- SbomProcessor: Represents an SBOM processor that defines the process of
                 analyzing SBOMs.
- SbomProcessorStatus: Represents the status of the SBOM processor.
"""
from enum import StrEnum
from dataclasses import dataclass
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.event import Event
from main.data_types.dependency_scorer import StepResponse
from main.data_types.dependency_scorer import (SSFAPIFetcher,
                                               DependencyScorer,
                                               ScorecardAnalyzer)
from main.backend_communication import BackendCommunication


class SbomProcessorStates(StrEnum):
    """
    Represents the status of a job.
    """
    INITIALIZING = "Initializing"
    INACTIVE = "Inactive"
    VALIDATING = "Validating"
    PARSING = "Parsing"
    FETCH_DATABASE = "Fetching from Database"
    SSF_LOOKUP = "SSF Lookup"
    ANALYZING_SCORE = "Analyzing Score"
    FINAL_SCORE = "Final Score"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    UPLOADING_SCORES = "Uploading Scores"


@dataclass
class SbomProcessorStatus:
    """
    Represents the status of an SBOM processor.
    """
    current_state: str
    step_response: StepResponse = None


class SbomProcessor:
    """
    Represents an SBOM processor that defines the process of analyzing SBOMs.
    """
    on_status_update: Event[SbomProcessorStatus]
    sbom_processor_status: SbomProcessorStatus

    def __init__(self, backend_host: str):
        """
        Initializes an SBOM processor.
        """
        self.on_status_update = Event[SbomProcessorStatus]()
        self.sbom_processor_status = SbomProcessorStatus(
            SbomProcessorStates.INITIALIZING
            )
        self.backend_communication = BackendCommunication(
            self._event_callback, backend_host
            )

    def _event_callback(self, step_response: StepResponse) -> None:
        """
        Callback function for the event.

        Args:
            step_response (StepResponse): The response from the step.
        """
        if step_response == self.sbom_processor_status.step_response:
            return

        self.sbom_processor_status.step_response = step_response
        self.on_status_update.invoke(self.sbom_processor_status)

    def _set_event_start_state(self,
                               state: SbomProcessorStates,
                               step_response: StepResponse = None) -> None:
        """
        Sets the event state.

        Args:
            state (SbomProcessorStates): The state to set.
        """
        if (state == self.sbom_processor_status.current_state and
            step_response == self.sbom_processor_status.step_response):
            return

        if step_response is None:
            step_response = StepResponse(0, 0, 0, 0, state.value)

        self.sbom_processor_status.step_response = step_response
        self.sbom_processor_status.current_state = state
        self.on_status_update.invoke(self.sbom_processor_status)

    def _run_dependency_scorer(
            self, sbom: Sbom,
            dependency_scorer: DependencyScorer,
            state: SbomProcessorStates
            ) -> None:
        """
        Runs a dependency scorer.

        Args:
            sbom (Sbom): The SBOM to analyze.
            dependency_scorer (DependencyScorer): The dependency scorer to run.
        """
        unscored_dependencies: list[Dependency] = sbom.get_unscored_dependencies()
        if not unscored_dependencies:
            return

        self._set_event_start_state(
            state,
            StepResponse(
                len(unscored_dependencies), 0, 0, 0, state.value)
            )
        new_dependencies = dependency_scorer.score(
            unscored_dependencies
            )
        sbom.dependency_manager.update(new_dependencies)

        step_response = self.sbom_processor_status.step_response
        if step_response.batch_size != step_response.completed_items:
            step_response.completed_items = step_response.batch_size
            self._set_event_start_state(state, step_response)

    def analyze_sbom(self, sbom: Sbom) -> Sbom:
        """
        Analyzes an SBOM and scores its dependencies.

        Args:
            sbom (Sbom): The SBOM to analyze.
        """
        # 1. Get score from BackendScorer
        self._run_dependency_scorer(
            sbom,
            self.backend_communication.backend_fetcher,
            SbomProcessorStates.FETCH_DATABASE
            )
        # 2. Get score from SSFAPIScorer
        self._run_dependency_scorer(
            sbom,
            SSFAPIFetcher(self._event_callback),
            SbomProcessorStates.SSF_LOOKUP
            )
        # 3. Get score from ScorecardAnalyzer
        self._run_dependency_scorer(
            sbom,
            ScorecardAnalyzer(self._event_callback),
            SbomProcessorStates.ANALYZING_SCORE
            )
        # 4. Update database with new scores
        self._set_event_start_state(
            SbomProcessorStates.UPLOADING_SCORES
            )
        self.backend_communication.add_sbom(sbom)
        # 5. Return the analyzed SBOM
        batch_size = len(sbom.get_dependencies_by_filter(lambda x: True))
        completed_items = batch_size
        success_count = len(sbom.get_scored_dependencies())
        failed_count = batch_size - success_count

        self._set_event_start_state(
            SbomProcessorStates.COMPLETED,
            StepResponse(
                batch_size, completed_items, success_count, failed_count,
                SbomProcessorStates.COMPLETED.value
                )
            )
        return sbom

    def lookup_stored_sboms(self) -> list[str]:
        """
        Looks up stored SBOMs in database

        Returns:
            list[str]: The list of the SBOM names
        """
        # Look up stored SBOMs
        self._set_event_start_state(SbomProcessorStates.FETCH_DATABASE)
        sbom_names = self.backend_communication.get_sbom_names()
        self._set_event_start_state(SbomProcessorStates.COMPLETED)
        return sbom_names

    def lookup_previous_sboms(self, name: str) -> list[Sbom]:
        """
        Looks up previously analyzed SBOMs.

        Args:
            name (str): The name of the SBOM to look up.

        Returns:
            list[dict]: The list of the SBOMs with the same name.
        """
        self._set_event_start_state(SbomProcessorStates.FETCH_DATABASE)
        sboms = self.backend_communication.get_sboms_by_name(name)
        self._set_event_start_state(SbomProcessorStates.COMPLETED)
        return sboms
