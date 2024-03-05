import requests


def add_sbom_results(sbom_json: dict):
    resp = requests.post("http://127.0.0.1:5080/add_SBOM", json=sbom_json)
    print(resp)


if __name__ == "__main__":
    sbom_json = {
        "serialNumber": "thisisaserialnumber",
        "version": "1",
        "name": "thisisaname",
        "repo_version": "1.0.0",
        "components": [
            {
                "name": "dep1",
                "version": "1.2.1",
                "score": 3.5,
                "checks": [
                    {
                        "name": "check1",
                        "details": "details1",
                        "score": 2.3,
                        "reason": "reason1",
                    },{
                        "name": "check2",
                        "details": "details2",
                        "score": 4.3,
                        "reason": "reason2",
                    },{
                        "name": "check3",
                        "details": "details3",
                        "score": 5.1,
                        "reason": "reason3",
                    }
                ],
            },{
                "name": "dep2",
                "version": "2.2.1",
                "score": 4.5,
                "checks": [
                    {
                        "name": "check1",
                        "details": "details1",
                        "score": 2.1,
                        "reason": "reason1",
                    },{
                        "name": "check2",
                        "details": "details2",
                        "score": 3.3,
                        "reason": "reason2",
                    },{
                        "name": "check3",
                        "details": "details3",
                        "score": 7.1,
                        "reason": "reason3",
                    }
                ],
            },
        ],
    }
    add_sbom_results(sbom_json)
