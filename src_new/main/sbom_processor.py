"""
This module contains the SBOM processor class, which is responsible for processing SBOMs.

Classes:
- SbomProcessor: Represents an SBOM processor that defines the process of analyzing SBOMs.
- SbomProcessorStatus: Represents the status of the SBOM processor.
"""
from enum import StrEnum
from dataclasses import dataclass
from data_types.sbom_types.sbom import Sbom
from data_types.event import Event
from data_types.dependency_scorer import StepResponse
from data_types.dependency_scorer import SSFAPIFetcher, DependencyScorer, ScorecardAnalyzer
from backend_communication import add_sbom, get_sboms_by_name, get_sbom_names, BackendFetcher


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

    def __init__(self):
        """
        Initializes an SBOM processor.
        """
        self.on_status_update = Event[SbomProcessorStatus]()
        self.sbom_processor_status = SbomProcessorStatus(SbomProcessorStates.INITIALIZING)


    def _event_callback(self, step_response: StepResponse) -> None:
        """
        Callback function for the event.

        Args:
            step_response (StepResponse): The response from the step.
        """
        self.sbom_processor_status.step_response = step_response
        self.on_status_update.invoke(self.sbom_processor_status)

    def _set_event_state(self, state: SbomProcessorStates) -> None:
        """
        Sets the event state.

        Args:
            state (SbomProcessorStates): The state to set.
        """
        self.sbom_processor_status.current_state = state
        self.on_status_update.invoke(self.sbom_processor_status)

    def _run_dependency_scorer(self, sbom: Sbom, dependency_scorer: DependencyScorer) -> None:
        """
        Runs a dependency scorer.

        Args:
            sbom (Sbom): The SBOM to analyze.
            dependency_scorer (DependencyScorer): The dependency scorer to run.
        """
        dependency_scorer.on_step_complete.subscribe(self._event_callback)
        current_unscored_dependencies = sbom.dependency_manager.get_unscored_dependencies()
        new_dependencies = dependency_scorer.score(current_unscored_dependencies)
        sbom.dependency_manager.update(new_dependencies)

    def analyze_sbom(self, sbom: Sbom) -> Sbom:
        """
        Analyzes an SBOM and scores its dependencies.

        Args:
            sbom (Sbom): The SBOM to analyze.
        """
        # TODO
        # 1. Get score from BackendScorer
        self._set_event_state(SbomProcessorStates.FETCH_DATABASE)
        self._run_dependency_scorer(sbom, BackendFetcher())
        # 2. Get score from SSFAPIScorer
        self._set_event_state(SbomProcessorStates.SSF_LOOKUP)
        self._run_dependency_scorer(sbom, SSFAPIFetcher())
        # 3. Get score from ScorecardAnalyzer
        self._set_event_state(SbomProcessorStates.ANALYZING_SCORE)
        self._run_dependency_scorer(sbom, ScorecardAnalyzer())
        # 4. Update database with new scores
        self._set_event_state(SbomProcessorStates.COMPLETED)
        add_sbom(sbom)
        return sbom

    def lookup_stored_sboms(self) -> list[str]:
        """
        Looks up stored SBOMs in database

        Returns:
            list[str]: The list of the SBOM names
        """
        # Look up stored SBOMs
        return get_sbom_names()

    def lookup_previous_sboms(self, name: str) -> list[Sbom]:
        """
        Looks up previously analyzed SBOMs.

        Args:
            name (str): The name of the SBOM to look up.
        
        Returns:
            list[dict]: The list of the SBOMs with the same name.
        """
        return get_sboms_by_name(name)
