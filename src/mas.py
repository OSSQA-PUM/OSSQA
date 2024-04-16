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
from backend_communication import get_sbom
from util import UserRequirements
import input_analyzer
import json


def analyze_sbom(sbom: dict, requirements: UserRequirements) -> list[list[str, int, str]]:
    """
    This function is called by the frontend API and calls 
    for SSFAnalyser and FSC.
    
    Args:
        sbom (dict): The SBOM to be analyzed.
        requirements (UserRequirements): The user-defined requirements 
                                        for the analysis.
        
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
    old_results = get_sbom(name)
    return old_results


def validate_input(sbom, requirements=None):
    try:
        sbom_dict = json.loads(sbom)
    except TypeError:  # if the sbom is not a string it is a dict
        sbom_dict = json.loads(sbom["sbom"])
    if requirements is None:
        requirements = UserRequirements()
    valid = input_analyzer.validate_input(sbom_dict, requirements)
    if valid:
        result = analyze_sbom(sbom_dict, requirements)
        return result
