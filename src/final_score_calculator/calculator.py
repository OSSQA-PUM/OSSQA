"""
This file contains a calculator for calculating final scores based on 
the scores of dependencies.
"""

import json
from src.util import Dependency

# Temporary data types until we create more modules and proper data types
FinalScore = list[str, int, str]  # (name, score, repository)
Score = list[str, int]  # (name, score)


def calculate_final_scores(dependencies: list[Dependency]) -> list[FinalScore]:
    """
    Calculates final scores based on the scores of dependencies.
    Each final score is the minimum of the dependency scores of the same type.

    Args:
        dependencies (list[Dependency]): 
        A list of Dependency objects representing the dependencies.

    Returns:
        list[FinalScore]: 
        A list of FinalScore objects containing the calculated final scores.
    """
    scores = list[FinalScore]()

    if not dependencies:
        return scores

    baseline: Dependency = dependencies[0]
    for check in baseline.dependency_score["checks"]:
        scores.append([check["name"], check["score"], baseline.url])

    for dependency in dependencies:
        dep_scores = dependency.dependency_score["checks"]
        for score_idx, dep_score in enumerate(dep_scores):
            curr_score = scores[score_idx][1]

            if dep_score["score"] < curr_score:
                # Replace current minimum score with dependency score
                scores[score_idx][1] = dep_score["score"]
                scores[score_idx][2] = dependency.url
    
    return scores

if __name__ == "__main__":
    with open(
        "E:/programming/OSSQA/src/final-score-calculator/example_repsonse.json"
        ) as f:
        score_card = json.load(f)
    dependency: Dependency = Dependency(
        json_component="", url="test", dependency_score=score_card
        )

    dependencies = [dependency]

    print(calculate_final_scores(dependencies))
