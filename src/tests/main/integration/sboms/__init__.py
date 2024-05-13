"""
This module contains downscaled SBOMs tailored to be used in
the integration tests.
"""
import json
from pathlib import Path

from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.scorecard import Scorecard

DIR_PATH = Path(__file__).parent
SBOM_PATH = DIR_PATH / "downscaled-ddmanager-controller.cdx.json"

SCORECARD = Scorecard({
    "date": "2024-04-15",
    "repo": {
        "name": "github.com/jonschlinkert/pad-left",
        "commit": "e521c7ba0d5d290b2cef7485af11b98dc96f2930"
    },
    "scorecard": {
        "version": "v4.13.1-273-g0b9dfb65",
        "commit": "0b9dfb656f1796c7c693ad74f5193657b6a81e0b"
    },
    "score": 3.2,
    "checks": [
        {
            "name": "Code-Review",
            "score": 1,
            "reason": "Found 3/28 approved changesets -- score normalized to 1",
            "details": None,
            "documentation": {
                "short": "Determines if the project requires human code review before pull requests (aka merge requests) are merged.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#code-review"
            }
        },
        {
            "name": "Maintained",
            "score": 0,
            "reason": "0 commit(s) and 0 issue activity found in the last 90 days -- score normalized to 0",
            "details": None,
            "documentation": {
                "short": "Determines if the project is \"actively maintained\".",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#maintained"
            }
        },
        {
            "name": "CII-Best-Practices",
            "score": 0,
            "reason": "no effort to earn an OpenSSF best practices badge detected",
            "details": None,
            "documentation": {
                "short": "Determines if the project has an OpenSSF (formerly CII) Best Practices Badge.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#cii-best-practices"
            }
        },
        {
            "name": "License",
            "score": 10,
            "reason": "license file detected",
            "details": [
                "Info: project has a license file: LICENSE:0",
                "Info: FSF or OSI recognized license: MIT License: LICENSE:0"
            ],
            "documentation": {
                "short": "Determines if the project has defined a license.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#license"
            }
        },
        {
            "name": "Signed-Releases",
            "score": -1,
            "reason": "no releases found",
            "details": None,
            "documentation": {
                "short": "Determines if the project cryptographically signs release artifacts.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#signed-releases"
            }
        },
        {
            "name": "Token-Permissions",
            "score": -1,
            "reason": "No tokens found",
            "details": None,
            "documentation": {
                "short": "Determines if the project's workflows follow the principle of least privilege.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#token-permissions"
            }
        },
        {
            "name": "Dangerous-Workflow",
            "score": -1,
            "reason": "no workflows found",
            "details": None,
            "documentation": {
                "short": "Determines if the project's GitHub Action workflows avoid dangerous patterns.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#dangerous-workflow"
            }
        },
        {
            "name": "Packaging",
            "score": -1,
            "reason": "packaging workflow not detected",
            "details": [
                "Warn: no GitHub/GitLab publishing workflow detected."
            ],
            "documentation": {
                "short": "Determines if the project is published as a package that others can easily download, install, easily update, and uninstall.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#packaging"
            }
        },
        {
            "name": "Binary-Artifacts",
            "score": 10,
            "reason": "no binaries found in the repo",
            "details": None,
            "documentation": {
                "short": "Determines if the project has generated executable (binary) artifacts in the source repository.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#binary-artifacts"
            }
        },
        {
            "name": "Pinned-Dependencies",
            "score": -1,
            "reason": "no dependencies found",
            "details": None,
            "documentation": {
                "short": "Determines if the project has declared and pinned the dependencies of its build process.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#pinned-dependencies"
            }
        },
        {
            "name": "Branch-Protection",
            "score": 0,
            "reason": "branch protection not enabled on development/release branches",
            "details": [
                "Warn: branch protection not enabled for branch 'master'"
            ],
            "documentation": {
                "short": "Determines if the default and release branches are protected with GitHub's branch protection settings.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#branch-protection"
            }
        },
        {
            "name": "Fuzzing",
            "score": 0,
            "reason": "project is not fuzzed",
            "details": [
                "Warn: no fuzzer integrations found"
            ],
            "documentation": {
                "short": "Determines if the project uses fuzzing.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#fuzzing"
            }
        },
        {
            "name": "Vulnerabilities",
            "score": 10,
            "reason": "0 existing vulnerabilities detected",
            "details": None,
            "documentation": {
                "short": "Determines if the project has open, known unfixed vulnerabilities.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#vulnerabilities"
            }
        },
        {
            "name": "Security-Policy",
            "score": 0,
            "reason": "security policy file not detected",
            "details": [
                "Warn: no security policy file detected",
                "Warn: no security file to analyze",
                "Warn: no security file to analyze",
                "Warn: no security file to analyze"
            ],
            "documentation": {
                "short": "Determines if the project has published a security policy.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#security-policy"
            }
        },
        {
            "name": "SAST",
            "score": 0,
            "reason": "SAST tool is not run on all commits -- score normalized to 0",
            "details": [
                "Warn: 0 commits out of 5 are checked with a SAST tool"
            ],
            "documentation": {
                "short": "Determines if the project uses static code analysis.",
                "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#sast"
            }
        }
    ]
})


def create_unscored_sbom() -> Sbom:
    with open(SBOM_PATH, "r", encoding="utf-8") as file:
        return Sbom(json.load(file))


def create_scored_sbom() -> Sbom:
    with open(SBOM_PATH, "r", encoding="utf-8") as file:
        sbom = Sbom(json.load(file))
    dependencies = []
    for dep in sbom.get_unscored_dependencies():
        dep_dict = dep.to_dict()
        if "platform_path" in dep_dict.keys():
            dep.dependency_score = SCORECARD
    sbom.update_dependencies(dependencies)
    return sbom


# from main.data_types.sbom_types.sbom import Sbom
# from main.data_types.sbom_types.scorecard import Scorecard

# SMALL_SBOM = Sbom({
#   "bomFormat": "CycloneDX",
#   "specVersion": "1.2",
#   "serialNumber": "urn:uuid:d7a0ac67-e0f8-4342-86c6-801a02437636",
#   "version": 1,
#   "metadata": {
#     "timestamp": "2021-05-16T17:10:53+02:00",
#     "component": {
#       "bom-ref": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
#       "type": "application",
#       "name": "github.com/ProtonMail/proton-bridge",
#       "version": "v1.8.0",
#       "purl": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
#       "externalReferences": [
#         {
#           "url": "https://github.com/ProtonMail/proton-bridge",
#           "type": "vcs"
#         }
#       ]
#     }
#   },
#   "components": [
#     {
#       "bom-ref": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
#       "type": "library",
#       "name": "github.com/andybalholm/cascadia",
#       "version": "v1.1.0",
#       "scope": "required",
#       "hashes": [
#         {
#           "alg": "SHA-256",
#           "content": "06eb8eeac49f40d151bb52e9a606c3db91ebdaf2d85b6e49bf11ece73cec2d3a"
#         }
#       ],
#       "licenses": [
#         {
#           "license": {
#             "id": "BSD-2-Clause",
#             "url": "https://spdx.org/licenses/BSD-2-Clause.html"
#           }
#         }
#       ],
#       "purl": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
#       "externalReferences": [
#         {
#           "url": "https://github.com/andybalholm/cascadia",
#           "type": "vcs"
#         }
#       ]
#     }
#   ]
# })
# SMALL_SCORECARD_DICT = {
#     "date": "2024-04-15",
#     "repo": {
#         "name": "github.com/jonschlinkert/pad-left",
#         "commit": "e521c7ba0d5d290b2cef7485af11b98dc96f2930"
#     },
#     "scorecard": {
#         "version": "v4.13.1-273-g0b9dfb65",
#         "commit": "0b9dfb656f1796c7c693ad74f5193657b6a81e0b"
#     },
#     "score": 3.2,
#     "checks": [
#         {
#             "name": "Code-Review",
#             "score": 1,
#             "reason": "Found 3/28 approved changesets -- score normalized to 1",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project requires human code review before pull requests (aka merge requests) are merged.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#code-review"
#             }
#         },
#         {
#             "name": "Maintained",
#             "score": 0,
#             "reason": "0 commit(s) and 0 issue activity found in the last 90 days -- score normalized to 0",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project is \"actively maintained\".",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#maintained"
#             }
#         },
#         {
#             "name": "CII-Best-Practices",
#             "score": 0,
#             "reason": "no effort to earn an OpenSSF best practices badge detected",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project has an OpenSSF (formerly CII) Best Practices Badge.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#cii-best-practices"
#             }
#         },
#         {
#             "name": "License",
#             "score": 10,
#             "reason": "license file detected",
#             "details": [
#                 "Info: project has a license file: LICENSE:0",
#                 "Info: FSF or OSI recognized license: MIT License: LICENSE:0"
#             ],
#             "documentation": {
#                 "short": "Determines if the project has defined a license.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#license"
#             }
#         },
#         {
#             "name": "Signed-Releases",
#             "score": -1,
#             "reason": "no releases found",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project cryptographically signs release artifacts.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#signed-releases"
#             }
#         },
#         {
#             "name": "Token-Permissions",
#             "score": -1,
#             "reason": "No tokens found",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project's workflows follow the principle of least privilege.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#token-permissions"
#             }
#         },
#         {
#             "name": "Dangerous-Workflow",
#             "score": -1,
#             "reason": "no workflows found",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project's GitHub Action workflows avoid dangerous patterns.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#dangerous-workflow"
#             }
#         },
#         {
#             "name": "Packaging",
#             "score": -1,
#             "reason": "packaging workflow not detected",
#             "details": [
#                 "Warn: no GitHub/GitLab publishing workflow detected."
#             ],
#             "documentation": {
#                 "short": "Determines if the project is published as a package that others can easily download, install, easily update, and uninstall.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#packaging"
#             }
#         },
#         {
#             "name": "Binary-Artifacts",
#             "score": 10,
#             "reason": "no binaries found in the repo",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project has generated executable (binary) artifacts in the source repository.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#binary-artifacts"
#             }
#         },
#         {
#             "name": "Pinned-Dependencies",
#             "score": -1,
#             "reason": "no dependencies found",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project has declared and pinned the dependencies of its build process.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#pinned-dependencies"
#             }
#         },
#         {
#             "name": "Branch-Protection",
#             "score": 0,
#             "reason": "branch protection not enabled on development/release branches",
#             "details": [
#                 "Warn: branch protection not enabled for branch 'master'"
#             ],
#             "documentation": {
#                 "short": "Determines if the default and release branches are protected with GitHub's branch protection settings.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#branch-protection"
#             }
#         },
#         {
#             "name": "Fuzzing",
#             "score": 0,
#             "reason": "project is not fuzzed",
#             "details": [
#                 "Warn: no fuzzer integrations found"
#             ],
#             "documentation": {
#                 "short": "Determines if the project uses fuzzing.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#fuzzing"
#             }
#         },
#         {
#             "name": "Vulnerabilities",
#             "score": 10,
#             "reason": "0 existing vulnerabilities detected",
#             "details": None,
#             "documentation": {
#                 "short": "Determines if the project has open, known unfixed vulnerabilities.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#vulnerabilities"
#             }
#         },
#         {
#             "name": "Security-Policy",
#             "score": 0,
#             "reason": "security policy file not detected",
#             "details": [
#                 "Warn: no security policy file detected",
#                 "Warn: no security file to analyze",
#                 "Warn: no security file to analyze",
#                 "Warn: no security file to analyze"
#             ],
#             "documentation": {
#                 "short": "Determines if the project has published a security policy.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#security-policy"
#             }
#         },
#         {
#             "name": "SAST",
#             "score": 0,
#             "reason": "SAST tool is not run on all commits -- score normalized to 0",
#             "details": [
#                 "Warn: 0 commits out of 5 are checked with a SAST tool"
#             ],
#             "documentation": {
#                 "short": "Determines if the project uses static code analysis.",
#                 "url": "https://github.com/ossf/scorecard/blob/0b9dfb656f1796c7c693ad74f5193657b6a81e0b/docs/checks.md#sast"
#             }
#         }
#     ]
# }

# for dependency in SMALL_SBOM.dependency_manager.get_unscored_dependencies():
#     dependency.dependency_score = Scorecard(SMALL_SCORECARD_DICT)
#     SMALL_SBOM.dependency_manager.update([dependency])
