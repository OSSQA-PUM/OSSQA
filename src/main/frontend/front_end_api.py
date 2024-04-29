"""
Front-end API for interacting with the SBOM processor and
performing various operations such as analyzing SBOMs,
looking up stored SBOMs, and retrieving previous SBOMs by name.
"""
import copy
from typing import Callable, Any
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import UserRequirements
from main.data_types.event import Event
from main.sbom_processor import SbomProcessor, SbomProcessorStatus
from main.frontend.final_score_calculator import calculate_final_scores


class FrontEndAPI:
    """
    Represents a front-end API for interacting with the SBOM processor and
    performing various operations such as analyzing SBOMs, looking up stored SBOMs,
    and retrieving previous SBOMs by name.
    """
    sbom_processor: SbomProcessor
    on_sbom_processor_status_update: Event[SbomProcessorStatus]

    def __init__(self, backend_host: str):
        """
        Initializes a front-end API.
        """
        self.sbom_processor = SbomProcessor(backend_host)
        self.on_sbom_processor_status_update = Event[SbomProcessorStatus]()
        self.sbom_processor.on_status_update.subscribe(self._update_sbom_processor_status)

    def _update_sbom_processor_status(self, sbom_processor_status: SbomProcessorStatus) -> None:
        """
        Invokes the SBOM processor status update event when the SBOM processor status is updated.

        Args:
            sbom_processor_status (SbomProcessorStatus): The SBOM processor status.
        """
        self.on_sbom_processor_status_update.invoke(sbom_processor_status)

    def subscribe_to_state_change(self, callback: Callable[[SbomProcessorStatus], Any]) -> None:
        """
        Subscribes to state change events.

        Args:
            callback: The callback function to be called on state change.
        """
        self.on_sbom_processor_status_update.subscribe(callback)

    def analyze_sbom(self, sbom: Sbom, user_requirements: UserRequirements) -> Sbom:
        """
        Analyzes an SBOM.

        Args:
            sbom (Sbom): The SBOM to analyze.
            user_requirements (UserRequirements): The user requirements.

        Returns:
            Sbom: The analyzed SBOM.
        """
        assert isinstance(sbom, Sbom), "sbom must be of type Sbom"
        assert isinstance(user_requirements, UserRequirements), \
        "user_requirements must be of type UserRequirements"

        sbom_copy: Sbom = copy.deepcopy(sbom)
        sbom_copy = self.sbom_processor.analyze_sbom(sbom_copy)

        scored_sbom: Sbom = calculate_final_scores(sbom_copy, user_requirements)

        return scored_sbom

    def lookup_stored_sboms(self) -> list[str]:
        """
        Looks up the names of stored SBOMs.

        Returns:
            list[str]: The list of names of stored SBOMs.
        """
        return self.sbom_processor.lookup_stored_sboms()

    def lookup_previous_sboms(self, name: str) -> list[Sbom]:
        """
        Looks up previous SBOMs with the specified name.

        Args:
            name (str): The name of the SBOM.

        Returns:
            list[Sbom]: The list of SBOMs with the specified name.
        """
        return self.sbom_processor.lookup_previous_sboms(name)
