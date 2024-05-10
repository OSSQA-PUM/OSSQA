"""
This module contains the function to calculate the final scores for the dependencies in the SBOM.
"""
import copy
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import UserRequirements
from main.data_types.sbom_types.dependency import Dependency

def grade_dependencies(sbom: Sbom, user_requirements: UserRequirements) -> Sbom:
    """
    Calculates the final scores for the dependencies in the SBOM.

    Args:
        sbom (Sbom): The SBOM to calculate the final scores for.
        user_requirements (UserRequirements): The user requirements
            to calculate the final scores with.

    Returns:
        Sbom: The SBOM with the final scores calculated.
    """
    sbom_copy = copy.deepcopy(sbom)

    for dependency in sbom_copy.dependency_manager.get_scored_dependencies():
        dependency.reach_requirement = _grade_dependency(dependency, user_requirements)
    return sbom_copy

def _grade_dependency(dependency: Dependency, user_requirements: UserRequirements) -> str:
    """
    Grades the dependency based on the user requirements.

    Args:
        dependency (Dependency): The dependency to grade.
        user_requirements (UserRequirements): The user requirements.

    Returns:
        str: The grade of the dependency.
    """
    requirements_dict: dict = user_requirements.to_dict()

    req_not_found: bool = False

    # Check if dependency failed
    for check in dependency.dependency_score.checks:
        passing_treshould:int = requirements_dict.get(check.name, None)
        if passing_treshould is None:
            req_not_found = True
            continue

        if passing_treshould > check.score:
            return "No"

    # Check if result not found
    if req_not_found:
        return "Test result not found"

    return "Yes"
