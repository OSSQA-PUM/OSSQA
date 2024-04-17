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


import json
from calculate_dependencies import parse_sbom, lookup_multiple_ssf, filter_database_dependencies, analyse_multiple_scores 
from final_score_calculator import calculator
from backend_communication import get_sbom, add_sbom, get_existing_dependencies
from util import UserRequirements, Dependency
from job_observer import JobModelSingleton
import input_analyzer

job_model = JobModelSingleton()

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

    needed_dependencies, failures, failure_reason = parse_sbom(sbom=sbom)
    total_dependency_count = len(needed_dependencies)

    scores = []

    new_scores, needed_dependencies = lookup_multiple_ssf(
        needed_dependencies=needed_dependencies)
    scores += new_scores

    database_response: list[Dependency] = get_existing_dependencies(needed_dependencies)

    new_scores, needed_dependencies = filter_database_dependencies(
        needed_dependencies, database_response)
    scores += new_scores

    analyzed_scores, needed_dependencies = analyse_multiple_scores(
        dependencies=needed_dependencies)
    scores += analyzed_scores

    # TODO send data that was downloaded internally
    add_sbom(sbom, scores)
    current_status = "Successfully got scores for " + f"{len(scores)}/" f"{total_dependency_count} dependencies. \n" \
                                                      f"{len(failures)}" + "dependencies failed to be parsed. \n" \
                                                                           f"{len(needed_dependencies)} dependencies could not be scored."
    job_model.set_attributes(message=current_status)

    scores = calculator.calculate_final_scores(scores, requirements)
    for i in range(len(scores)):
        for j in range(len(scores[0])):
            scores[i][j] = str(scores[i][j])
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
        sbom = sbom.replace("'", '"')
        sbom_dict = json.loads(sbom)["sbom"]
    except KeyError:  # if the sbom is not a string it is a dict
        sbom = sbom.replace("'", '"')
        sbom_dict = json.loads(sbom)
    if requirements is None:
        requirements = UserRequirements()
    valid = input_analyzer.validate_input(sbom_dict, requirements)
    if valid:
        result = analyze_sbom(sbom_dict, requirements)
        return result
