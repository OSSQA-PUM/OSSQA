import json
from pathlib import Path
from tests.unit_tests.scorecards.scorecards import PATHS
from data_types.sbom_types.scorecard import Scorecard

DIRECTORY = Path(__file__).parent

PATHS = [
    DIRECTORY / "dependency_pad_left.json",
]


def test():
    with open(PATHS[1], "r") as file:
        scorecard = json.load(file)
    s = Scorecard(scorecard)
    with open("dependency.json", "w") as file:
        json.dump(s.to_dict(), file, indent=4)
