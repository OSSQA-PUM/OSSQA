from calculator import calculate_final_scores


def test_calculator():
    dependencies = [
        ["repo_1", [
            ["category_1", 2],
            ["category_2", 1],
            ["category_3", 6],
        ]],
        ["repo_2", [
            ["category_1", 4],
            ["category_2", 8],
            ["category_3", 2],
        ]],
        ["repo_3", [
            ["category_1", 9],
            ["category_2", 2],
            ["category_3", 3],
        ]],
    ]

    final_scores = calculate_final_scores(dependencies)

    assert final_scores == [
        ["category_1", 2, "repo_1"],
        ["category_2", 1, "repo_1"],
        ["category_3", 2, "repo_2"],
    ]