import pytest

from main.data_types.user_requirements import (UserRequirements,
                                               RequirementsType)

REQ_TYPES = [req_type.value for req_type in RequirementsType]


@pytest.fixture(name="valid_empty_reqs")
def valid_empty_reqs_fixture() -> dict:
    return {}


@pytest.fixture(name="valid_filled_reqs")
def valid_filled_reqs_fixture() -> dict:
    return {
        RequirementsType.VULNERABILITIES: 4,
        RequirementsType.DEPENDENCY_UPDATE_TOOL: 7,
        RequirementsType.MAINTAINED: 5,
        RequirementsType.SECURITY_POLICY: 10,
        RequirementsType.LICENSE: -1,
        RequirementsType.CI_TESTS: 7,
        RequirementsType.FUZZING: 0,
        RequirementsType.SAST: 2,
        RequirementsType.BINARY_ARTIFACTS: 3,
        RequirementsType.BRANCH_PROTECTION: 9,
        RequirementsType.DANGEROUS_WORKFLOW: 5,
        RequirementsType.CODE_REVIEW: 6,
        RequirementsType.CONTRIBUTORS: 3,
        RequirementsType.PINNED_DEPENDENCIES: 1,
        RequirementsType.TOKEN_PERMISSIONS: 1,
        RequirementsType.PACKAGING: 5,
        RequirementsType.SIGNED_RELEASES: 8
    }


@pytest.fixture(name="invalid_type_reqs")
def invalid_type_reqs_fixture(valid_filled_reqs: dict) -> list[dict]:
    result = []

    for req_type in REQ_TYPES:
        reqs = valid_filled_reqs.copy()
        reqs[req_type] = True
        result.append(reqs)
    return result


@pytest.fixture(name="invalid_value_reqs")
def invalid_valid_reqs_fixture(valid_filled_reqs: dict) -> list[dict]:
    result = []
    for req_type in REQ_TYPES:
        reqs = valid_filled_reqs.copy()
        reqs[req_type] = -1
        result.append(reqs)
    for req_type in REQ_TYPES:
        reqs = valid_filled_reqs.copy()
        reqs[req_type] = 11
        result.append(reqs)
    return result


def test_valid_requirements(valid_filled_reqs: dict,
                            valid_empty_reqs: dict):
    try:
        UserRequirements(valid_filled_reqs)
    except TypeError:
        pytest.fail("Invalid requirement types!")
    except ValueError:
        pytest.fail("Invalid requirement values!")

    try:
        UserRequirements(valid_empty_reqs)
    except TypeError:
        pytest.fail("Invalid requirement types!")
    except ValueError:
        pytest.fail("Invalid requirement values!")
