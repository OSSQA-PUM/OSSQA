"""
Import file with code to be examined
"""

from pathlib import Path
import json
import pytest
from frontend_api import check_input_arguments, check_format_of_sbom
from util import UserRequirements

@pytest.fixture(scope="module")
def example_sbom() -> str:
    """
    Fixture for the example SBOM file.
    """
    return str(Path(__file__).parent.absolute() / "sboms" / "example-SBOM.json")


def test_integer_values() -> None:
    """
    Integer Value Testing:

        - Testing valid and invalid integer priority values.
    """
    result = True
    requirements: UserRequirements = UserRequirements()
    requirements.build_risk_assessment = -1
    requirements.source_risk_assessment = 1
    requirements.maintence = 1
    requirements.continuous_testing = 1
    requirements.code_vunerabilities = 1
    try:
        check_input_arguments(requirements)
        result = False
    except ValueError:
        pass

    requirements.build_risk_assessment = 11

    try:
        check_input_arguments(requirements)
        result = False
    except ValueError:
        pass

    assert result


def test_decimal_values() -> None:
    """
    Decimal Value Testing:

        - Testing decimal priority values
    """
    result = True
    requirements: UserRequirements = UserRequirements()
    requirements.build_risk_assessment = 0.5
    requirements.source_risk_assessment = 1
    requirements.maintence = 1
    requirements.continuous_testing = 1
    requirements.code_vunerabilities = 1
    try:
        check_input_arguments(requirements)
        result = False
    except ValueError:
        pass
    assert result


def test_valid_sbom(example_sbom) -> None:
    """
    Valid SBOM Testing:

        - Testing if correct format of SBOM
        - Testing if valid specVersion
        - Testing if valid serial number
    """
    # Testing if correct format of SBOM
    result = True
    sbom_file = open(example_sbom, encoding="utf-8")
    sbom_dict = json.load(sbom_file)
    try:
        check_format_of_sbom(sbom_dict)
    except SyntaxError:
        result = False
    except IndexError:
        result = False
    assert result
