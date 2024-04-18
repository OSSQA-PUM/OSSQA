"""
This file contains a calculator for calculating final scores based on 
the scores of dependencies.
"""

from util import Dependency, Checks, UserRequirements

# Temporary data types until we create more modules and proper data types
FinalScore = list[str, int, str]  # (name, score, repository)
Score = list[str, int]  # (name, score)


def calculate_final_scores(dependencies: list[Dependency], requirements: UserRequirements = None) -> list[FinalScore]:
    """
    Calculates final scores based on the scores of dependencies.
    Each final score is the minimum of the dependency scores of the same type.

    Args:
        dependencies (list[Dependency]): 
        A list of Dependency objects representing the dependencies.

        requirements (UserRequirements, optional):
        User-defined requirements for the analysis. Defaults to None.

    Returns:
        list[FinalScore]: 
        A list of FinalScore objects containing the calculated final scores.
    """
    if not requirements:
        requirements = UserRequirements()

    scores = list[FinalScore]()

    if not dependencies:
        return scores

    for dependency in dependencies:
        dependency: Dependency
        for check in dependency.dependency_score["checks"]:
            scores.append([check["name"], int(check["score"]), str(dependency.url)])
    return scores
