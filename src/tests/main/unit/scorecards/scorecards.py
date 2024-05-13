from pathlib import Path
from main.data_types.sbom_types.scorecard import ScorecardChecks

DIRECTORY = Path(__file__).parent

PATHS = [
    DIRECTORY / "docker.json",
    DIRECTORY / "pad-left.json",
    DIRECTORY / "pytorch.json",
    DIRECTORY / "react.json",
    DIRECTORY / "OSSQA-PUM-scorecard.json"
]

UNPARSABLE_SCORECARDS = [
    {
        "date": "2021-10-10",
        "checks": [
            {
                "name": ScorecardChecks.BINARY_ARTIFACTS,
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.BRANCH_PROTECTION,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.CI_TESTS,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.CONTRIBUTORS,
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.DANGEROUS_WORKFLOW,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.DEPENDENCY_UPDATE_TOOL,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.VULNERABILITIES,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.SAST,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.SECURITY_POLICY,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.SIGNED_RELEASES,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.TOKEN_PERMISSIONS,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.VULNERABILITIES,
                "score": 0,
                "details": []
            },
            {
                "name": ScorecardChecks.BINARY_ARTIFACTS,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.CODE_REVIEW,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason1",
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
    }
]


OUT_OF_BOUNDS_SCORECARDS = [
    {
        "date": "2021-10-10",
        "score": -2,
        "checks": [
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 11,
        "checks": [
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 0,
                "reason": "reason3",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": -2,
                "reason": "reason1",
                "details": []
            }
        ]
    },
    {
        "date": "2021-10-10",
        "score": 0,
        "checks": [
            {
                "name": ScorecardChecks.CII_BEST_PRACTICES,
                "score": 11,
                "reason": "reason1",
                "details": []
            }
        ]
    }
]
