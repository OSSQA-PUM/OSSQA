import pytest

from data_types.user_requirements import UserRequirements, RequirementsType

REQ_TYPES = [req_type.value for req_type in RequirementsType]


@pytest.fixture(name="valid_empty_reqs")
def valid_empty_reqs_fixture() -> dict:
    return {}


@pytest.fixture(name="valid_filled_reqs")
def valid_filled_reqs_fixture() -> dict:
    return {
        RequirementsType.CODE_VULNERABILITIES: 0,
        RequirementsType.MAINTENANCE: 3,
        RequirementsType.CONTINUOUS_TESTING: 6,
        RequirementsType.SOURCE_RISK_ASSESSMENT: 9,
        RequirementsType.BUILD_RISK_ASSESSMENT: 10,
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
def invalid_valud_reqs_fixture(valid_filled_reqs: dict) -> list[dict]:
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


def test_invalid_requirements(invalid_type_reqs: list[dict],
                              invalid_value_reqs: list[dict]):
    for type_reqs in invalid_type_reqs:
        with pytest.raises(TypeError):
            UserRequirements(type_reqs)

    for value_reqs in invalid_value_reqs:
        with pytest.raises(ValueError):
            UserRequirements(value_reqs)
