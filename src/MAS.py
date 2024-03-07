"""
This module contains functions for analyzing SBOMs and retrieving old results.

Functions:
- analyze_sbom(sbom: dict, requirements: list[int]) -> list[float]: 
This function is called by the frontend API and calls for SSFAnalyser and FSC. 
It analyzes the given SBOM and returns the final scores 
based on the requirements.

- get_old_results(sbom: dict): This function calls the backend API to get 
the old results for a given SBOM.
"""

import calculate_dependencies
from final_score_calculator import calculator
from backend_communication import get_existing_results

def analyze_sbom(sbom: dict, requirements: list[int]) -> list[float]:
    """
    This function is called by the frontend API and calls 
    for SSFAnalyser and FSC.
    
    Args:
        sbom (dict): The SBOM to be analyzed.
        requirements (list[float]): The requirements for the SBOM.
        
    Returns:
        list[float]: The final scores.
    """
    scored = calculate_dependencies.get_dependencies(sbom)[0]
    scores = calculator.calculate_final_scores(scored, requirements)
    return scores


def get_old_results(sbom: dict):
    """
    This function calls the backend API to get the old results 
    for a given SBOM.
    
    Args:
        sbom (dict): The SBOM for which old results are to be fetched.
        
    Returns:
        dict: The old results.
    """
    name = sbom['metadata']['name'] + sbom['metadata']['version']
    old_results = backend_communication.get_existing_results(name)
    return old_results
