"""
This module contains functions for communicating with the database.

Functions:
- add_sbom: Adds an SBOM, its dependencies, and their scores to the database.
- get_sboms_by_name: Gets all versions of a SBOM:s with a specific name.
- get_sbom_names: Returns the names of all the SBOMs in the database.
- get_existing_dependencies: Gets saved dependencies from the database.
"""
from data_types.sbom_types.dependency import Dependency
from data_types.sbom_types.sbom import Sbom
from data_types.dependency_scorer import DependencyScorer, StepResponse


async def add_sbom(sbom: Sbom) -> None:
    """
    Adds an SBOM, its dependencies, and their scores to the database.
    
    Args:
        sbom (Sbom): The SBOM to add to the database.
    """
    # TODO
    # 1. Convert the SBOM dependencies to json
    # 2. POST the json data to "localhost:5090/add_SBOM"
    pass


def get_sboms_by_name(name: str) -> list[Sbom]:
    """
    Gets all versions of a SBOM:s with a specific name.

    Args:
        name (str): The name of the SBOM:s.
    
    Returns:
        list[Sbom]: A list containing the SBOM:s.
    """
    # TODO
    # 1. Request SBOMs with the specified name from the database.
    # 2. Create a list of Sbom objects from the response json.
    dummy_list = list[Sbom]()
    return dummy_list


def get_sbom_names() -> list[str]:
    """
    Returns the names of all the SBOMs in the database.
    
    Returns:
        list[str]: A list containing the names of all the 
    """
    # TODO
    # 1. Request the names from the database
    # 2. Parse the response to a list of strings
    # 3. Return the list
    dummy_str = ""
    return [dummy_str]

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

    def _get_existing_dependencies(self, dependencies: list[Dependency]) -> list[Dependency]:
        """
        Gets saved dependencies from the database
        
        Args:
        dependencies (list[Dependency]): The dependencies to check

        Returns:
            list[Dependency]: The existing dependencies in the database
        """
        # TODO
        # 1. Loop through all dependencies
        # 2. Lookup dependency in the database
        # 3. Return list of all dependencies that exist in the database
        new_dependencies = []
        return new_dependencies
