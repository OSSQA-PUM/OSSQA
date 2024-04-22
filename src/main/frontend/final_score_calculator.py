"""
This module contains the function to calculate the final scores for the dependencies in the SBOM.
"""
import copy
from data_types.sbom_types.sbom import Sbom
from data_types.user_requirements import UserRequirements

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
    # TODO: Implement final score calculation
    return sbom_copy
