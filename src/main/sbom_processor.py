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

        Args:
            backend_host (str): The host of the backend.
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
        self.sbom_processor_status.step_response = step_response
        self.on_status_update.invoke(self.sbom_processor_status)

    def _set_event_start_state(self,
                               state: SbomProcessorStates,
                               step_response: StepResponse = None) -> None:
        """
        Sets the event start state.

        Args:
            state (SbomProcessorStates): The state to set.
            step_response (StepResponse): The response from the step.
        """
        if step_response:
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
            state (SbomProcessorStates): The state to set.
        """
        current_unscored_dependencies = \
            sbom.dependency_manager.get_dependencies_by_filter(
                lambda dependency: not dependency.scorecard
            )
        self._set_event_start_state(
            state,
            StepResponse(
                len(current_unscored_dependencies), 0, 0, 0, state.value)
            )
        new_dependencies = dependency_scorer.score(
            current_unscored_dependencies
            )
        sbom.dependency_manager.update(new_dependencies)

    def analyze_sbom(self, sbom: Sbom) -> Sbom:
        """
        Analyzes the given SBOM (Software Bill of Materials) by running
        various dependency scorers and updating the scores in the database.

        Parameters:
        sbom (Sbom): The SBOM to be analyzed.

        Returns:
        Sbom: The analyzed SBOM with updated scores.

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
            SbomProcessorStates.UPLOADING_SCORES,
            StepResponse(
                len(sbom.get_scored_dependencies()),
                0, 0, 0, SbomProcessorStates.UPLOADING_SCORES.value)
            )
        self.backend_communication.add_sbom(sbom)
        all_deps = len(sbom.get_dependencies_by_filter(lambda x: True))
        self._set_event_start_state(
            SbomProcessorStates.COMPLETED,
            StepResponse(
                all_deps,
                all_deps,
                len(sbom.get_scored_dependencies()),
                len(sbom.get_failed_dependencies()),
                SbomProcessorStates.COMPLETED.value)
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
            list[Sbom]: The list of the SBOMs with the same name.
        """
        self._set_event_start_state(SbomProcessorStates.FETCH_DATABASE)
        sboms = self.backend_communication.get_sboms_by_name(name)
        self._set_event_start_state(SbomProcessorStates.COMPLETED)
        return sboms
