# Temporary data types until we create more modules and proper data types
FinalScore = list[str, int, str]  # (name, score, repository)
Score = list[str, int]  # (name, score)
Dependency = list[str, list[Score]] # (repository, scores)


def calculate_final_scores(dependencies: list[Dependency]) -> list[FinalScore]:
    """
    Calculates final scores based on the scores of dependencies.
    Each final score is the minimum of the dependency scores of the same type.
    """
    scores = list[FinalScore]()

    for dependency in dependencies:
        if not scores:
            scores = [[name, score, dependency[0]] for name, score in dependency[1]]
        else:
            for score_idx in range(len(dependency[1])):
                (_, dep_score) = dependency[1][score_idx]
                (_, curr_score, _) = scores[score_idx]

                if dep_score < curr_score:
                    # Replace current minimum score with dependency score
                    scores[score_idx][1] = dep_score
                    scores[score_idx][2] = dependency[0]
    
    return scores