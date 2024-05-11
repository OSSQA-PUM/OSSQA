import pytest
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard, ScorecardChecks
from main.frontend.dependency_grader import grade_dependencies
from main.data_types.user_requirements import UserRequirements
from main.data_types.sbom_types.dependency_manager import DependencyManager

minimal_sbom_dict = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.2",
    "serialNumber": "urn:uuid:d7a0ac67-e0f8-4342-86c6-801a02437636",
    "version": 1,
    "metadata": {
        "timestamp": "2021-05-16T17:10:53+02:00",
        "tools": [
            ],
            "component": {
                "bom-ref": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
                "type": "application",
                "name": "github.com/ProtonMail/proton-bridge",
                "version": "v1.8.0",
                "purl": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
                "externalReferences": [
                    {
                        "url": "https://github.com/ProtonMail/proton-bridge",
                        "type": "vcs"
                    }
                ]
            }
        },
    "components": [
        ]
}

scorecard_1: Scorecard = Scorecard({
        "date": "2021-05-16T17:10:53+02:00",
        "score": 10,
        "checks": [
            {
                "name": ScorecardChecks.DEPENDENCY_UPDATE_TOOL.value,
                "score": 8,
                "reason": "Check",
                "details": "Check"
            },
            {
                "name": ScorecardChecks.FUZZING.value,
                "score": 10,
                "reason": "Check",
                "details": "Check"
            },
            {
                "name": ScorecardChecks.LICENSE.value,
                "score": 5,
                "reason": "Check",
                "details": "Check"
            }
        ]
    })
dep_one = Dependency("component_1", "dep_1", "1.0.0", scorecard_1)


scorecard_2: Scorecard = Scorecard({
    "date": "2021-05-16T17:10:53+02:00",
    "score": 10,
    "checks": [
        {
            "name": ScorecardChecks.DEPENDENCY_UPDATE_TOOL.value,
            "score": 8,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.FUZZING.value,
            "score": 8,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.LICENSE.value,
            "score": 9,
            "reason": "Check",
            "details": "Check"
        }
    ]
})
dep_two = Dependency("component_2", "dep_2", "1.0.0", scorecard_2)

scorecard_3: Scorecard = Scorecard({
    "date": "2021-05-16T17:10:53+02:00",
    "score": 10,
    "checks": [
        {
            "name": ScorecardChecks.DEPENDENCY_UPDATE_TOOL.value,
            "score": 10,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.FUZZING.value,
            "score": 10,
            "reason": "Check",
            "details": "Check"
        }
    ]
})
dep_three = Dependency("component_3", "dep_3", "1.0.0", scorecard_3)

scorecard_4: Scorecard = Scorecard({
    "date": "2021-05-16T17:10:53+02:00",
    "score": 10,
    "checks": [
        {
            "name": ScorecardChecks.DEPENDENCY_UPDATE_TOOL.value,
            "score": 8,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.FUZZING.value,
            "score": 6,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.LICENSE.value,
            "score": 9,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.BINARY_ARTIFACTS.value,
            "score": 1,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.CII_BEST_PRACTICES.value,
            "score": 5,
            "reason": "Check",
            "details": "Check"
        },
        {
            "name": ScorecardChecks.CI_TESTS.value,
            "score": 6,
            "reason": "Check",
            "details": "Check"
        }
    ]
})
dep_four = Dependency("component_4", "dep_4", "1.0.0", scorecard_4)


def test_single_pass():
    """
    Test that the reach_requirement field is set to "Yes" when the dependency
    meets the user requirements
    """
    sbom: Sbom = Sbom(minimal_sbom_dict)
    sbom.dependency_manager.update([dep_one])

    user_requirements_pass: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 8,
            "fuzzing": 10,
            "license": 3
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements_pass)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "Yes"


def test_single_fail():
    """
    Test that the reach_requirement field is set to "No" when the dependency
    does not meet the user requirements
    """
    sbom: Sbom = Sbom(minimal_sbom_dict)
    sbom.dependency_manager.update([dep_one])

    user_requirements_fail:  UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 8,
            "fuzzing": 10,
            "license": 6
        }
    )
    graded_sbom = grade_dependencies(sbom, user_requirements_fail)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "No"


def test_single_not_found():
    """
    Test that the reach_requirement field is set to "Test 
    result not found" when the dependency does not have a scorecard
    """
    sbom: Sbom = Sbom(minimal_sbom_dict)
    sbom.dependency_manager.update([dep_one])

    user_requirements: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 4,
            "fuzzing": 10,
            "license": 5,
            "binary_artifacts": 2
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "Test result not found"


def test_single_edge_case():
    """
    Test that the reach_requirement field is set correctly when along the edge
    """
    sbom: Sbom = Sbom(minimal_sbom_dict)
    sbom.dependency_manager.update([dep_four])

    user_requirements: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 4,
            "fuzzing": 10,
            "license": 7,
            "binary_artifact": 4,
            "cii_best_practices": 5,
            "ci_tests": 0
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "No"

    user_requirements: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 8,
            "fuzzing": 4,
            "license": 9,
            "binary_artifact": 1,
            "cii_best_practices": 5,
            "ci_tests": 6
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "Yes"

    user_requirements: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 8,
            "fuzzing": 4,
            "license": 9,
            "packaging": 1,
            "binary_artifact": 1,
            "cii_best_practices": 5,
            "ci_tests": 6
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    assert scored_dependencies[0].reach_requirement == "Test result not found"

def test_multiple():
    """
    Test that the reach_requirement field is set to the correct value when
    multiple dependencies are graded
    """

    sbom: Sbom = Sbom(minimal_sbom_dict)
    sbom.dependency_manager.update([dep_one, dep_two, dep_three, dep_four])

    user_requirements: UserRequirements = UserRequirements(
        {
            "dependency_update_tool": 8,
            "fuzzing": 6,
            "license": 7
        }
    )

    graded_sbom = grade_dependencies(sbom, user_requirements)
    dep_manager: DependencyManager = graded_sbom.dependency_manager
    scored_dependencies = dep_manager.get_scored_dependencies()
    print(len(scored_dependencies))
    assert scored_dependencies[0].reach_requirement == "No"
    assert scored_dependencies[1].reach_requirement == "Yes"
    assert scored_dependencies[2].reach_requirement == "Test result not found"
    assert scored_dependencies[3].reach_requirement == "Yes"
