"""
This module contains the function to calculate the final scores for the dependencies in the SBOM.
"""
import copy
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import UserRequirements
from main.data_types.sbom_types.dependency import Dependency

def grade_dependencies(sbom: Sbom, user_requirements: UserRequirements) -> Sbom:
    """
    Grades the dependencies in the SBOM based on the user requirements.

    Args:
        sbom (Sbom): The SBOM to grade.
        user_requirements (UserRequirements): The user requirements.

    Returns:
        Sbom: The graded SBOM.
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
    dependency_scores: dict = dependency.dependency_score.to_dict()
    checks: dict = {}

    for check in dependency_scores["checks"]:
        checks[check["name"]] = check["score"]

    found_all_checks: bool = True

    # Check if dependency failed
    for req_name, req_score in user_requirements.get_listed_requirements():
        if req_score == -1:
            continue

        check_score = checks.get(req_name, None)
        if check_score is None:
            found_all_checks = False
            continue

        if check_score < req_score:
            return "No"
            

    # Check if result not found
    if not found_all_checks:
        return "Test result not found"
    
    return "Yes"
