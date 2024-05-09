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

    #print("Old dependencies: \n" + str(sbom_copy.dependency_manager.get_scored_dependencies()))

    for dependency in sbom_copy.dependency_manager.get_scored_dependencies():
        listed_requirements = user_requirements.get_listed_requirements()
        for check in dependency.dependency_score.checks:
                checks.append(check.name)
        for requirement in listed_requirements:
            if not requirement[0] in checks:
                if requirement[1] > -1:
                    dependency.reach_requirement = "Test result not found"
            else:
                for check1 in checks:
                    if check1 == requirement[0]:
                        if (requirement[1] <= dependency.dependency_score.checks[0].score and
                            dependency.reach_requirement != "No" and 
                            dependency.reach_requirement != "Test result not found"):
                            dependency.reach_requirement = "Yes"
                        else:
                            print("Req: " + str(requirement[1]) + " for " + str(requirement[0]) + " and score: " + str(dependency.dependency_score.checks[0].score) + " for " + str(dependency.dependency_score.checks[0].name))
                            dependency.reach_requirement = "No"
                
        checks.clear()

    # TODO: Implement final score calculation
    return sbom_copy
