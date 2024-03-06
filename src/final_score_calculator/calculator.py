"""
This file contains a calculator for calculating final scores based on 
the scores of dependencies.
"""

import json
from util import Dependency, Checks

# Temporary data types until we create more modules and proper data types
FinalScore = list[str, int, str]  # (name, score, repository)
Score = list[str, int]  # (name, score)


def calculate_final_scores(
        dependencies: list[Dependency], 
        requirements: list[float] = None
        ) -> list[FinalScore]:
    """
    Calculates final scores based on the scores of dependencies.
    Each final score is the minimum of the dependency scores of the same type.

    Args:
        dependencies (list[Dependency]): 
        A list of Dependency objects representing the dependencies.

        requirements (list[float], optional):
        A list of user requirements for the final scores.

    Returns:
        list[FinalScore]: 
        A list of FinalScore objects containing the calculated final scores.
    """
    if not requirements:
        requirements = [10] * 5

    scores = list[FinalScore]()

    if not dependencies:
        return scores

    baseline: Dependency = dependencies[0]
    for check in Checks.all():
        current_baseline_check = baseline.get_check(check)
        scores.append([check.value, current_baseline_check["score"], baseline.url])
    
    for dependency in dependencies:
        for score in scores:
            current_depency_score = dependency.get_check(score[0])["score"]
            if score[1] > current_depency_score:
                # Replace current minimum score with dependency score
                score[1] = current_depency_score
                score[2] = dependency.url
    
    return scores

if __name__ == "__main__":
    with open(
        "E:/programming/OSSQA/src/final-score-calculator/example_repsonse.json",
        encoding="utf-8"
        ) as f:
        score_card = json.load(f)
    dependency: Dependency = Dependency(
        json_component={}, url="test", dependency_score=score_card
        )

    dependencies = [dependency]

    print(calculate_final_scores(dependencies))
