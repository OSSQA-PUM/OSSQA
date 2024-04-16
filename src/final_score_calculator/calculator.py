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

    baseline: Dependency = dependencies[0]
    for dependency in dependencies:
        for check in Checks.all():
            scores.append([check, int(dependency.dependency_score["score"]), str(dependency.url)])

    # for check in Checks.all():
    #     current_baseline_check = baseline.get_check(check)
    #     scores.append([check.value,
    #                    current_baseline_check["score"],
    #                    baseline.url, baseline.])
    #
    # for dependency in dependencies:
    #     for score in scores:
    #         current_depedency_score = dependency.get_check(score[0])["score"]
    #         if score[1] > current_depedency_score:
    #             # Replace current minimum score with dependency score
    #             score[1] = current_depedency_score
    #             score[2] = dependency.url

    return scores
