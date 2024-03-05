#import backend_communication
import calculate_dependencies
import final_score_calculator.calculator as calculator

def analyze_sbom(sbom: dict, requirements: list[int]) -> float:
    """
    This function is called by frontend API and calls for SSFAnalyser and FSC
    Args:
        sbom (dict): The SBOM to be analyzed
        requirements (list[float]): The requirements for the SBOM
    Returns:
        dictionary: The final scores
    """
    score_dict = calculate_dependencies.get_dependencies(sbom)
    score = calculator.calculate_final_scores(score_dict, requirements)
    return score


def get_old_results(sbom: dict):
    """
    This functions calls the backend API to get the old results
    Args:
        sbom (dict): The SBOM which old results are to be fetched
    Returns:
        dict: The old results
    """
    name = sbom['metadata']['name'] + sbom['metadata']['version']
    #old_results = backend_communication.get_existing_results(name)
    #return old_results
    return ["trash", "trash", "trash"] #REMOVE