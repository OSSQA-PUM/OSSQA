from pathlib import Path

DIRECTORY = Path(__file__).parent

PATHS = [
    DIRECTORY / "docker.json",
    DIRECTORY / "pad-left.json",
    DIRECTORY / "pytorch.json",
    DIRECTORY / "react.json"
]

UNPARSABLE_SCORECARDS = [
    {
        "date": "2021-10-10",
        "checks": [
            {
                "name": "check1",
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
                "reason": "reason1",
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
                "score": 0,
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
                "score": 0,
                "reason": "reason1",
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
        "score": -1,
        "checks": [
            {
                "name": "check1",
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
                "score": 0,
                "reason": "reason1",
                "details": []
            },
            {
                "name": "check2",
                "score": 0,
                "reason": "reason2",
                "details": []
            },
            {
                "name": "check3",
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
                "name": "check1",
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
                "name": "check1",
                "score": 11,
                "reason": "reason1",
                "details": []
            }
        ]
    }
]