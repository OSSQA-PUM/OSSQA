"""
This module contains the function to calculate the final scores for the dependencies in the SBOM.
"""
import copy
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import UserRequirements

def calculate_final_scores(sbom: Sbom, user_requirements: UserRequirements) -> Sbom:
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
    checks = []
    check_names = []
    names_score = []

    #print("Old dependencies: \n" + str(sbom_copy.dependency_manager.get_scored_dependencies()))

    for dependency in sbom_copy.dependency_manager.get_scored_dependencies():
        listed_requirements = user_requirements.get_listed_requirements()
        for ch in dependency.dependency_score.checks:
            check_names.append(ch.name)

        for check in dependency.dependency_score.checks:
            names_score.append(check.name)
            names_score.append(check.score)
            copy_names_score = names_score.copy()
            checks.append(copy_names_score)
            names_score.clear()

        for requirement in listed_requirements:
            if not requirement[0] in check_names:
                if requirement[1] > -1:
                    dependency.reach_requirement = "Test result not found"
            else:
                for check1 in checks:
                    if check1[0] == requirement[0]:
                        if (requirement[1] <= check1[1] and
                            dependency.reach_requirement != "No" and 
                            dependency.reach_requirement != "Test result not found"):
                            dependency.reach_requirement = "Yes"
                        else:
                            if requirement[1] > check1[1]:
                                dependency.reach_requirement = "No"
                
        checks.clear()

    # TODO: Implement final score calculation
    return sbom_copy
