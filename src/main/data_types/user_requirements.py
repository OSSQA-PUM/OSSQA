"""
This module contains every datatype related to user-specified
requirements.
"""
from enum import StrEnum


class RequirementsType(StrEnum):
    """
    Mappings between strings and OpenSSF Scorecard check categories.
    """
    CODE_VULNERABILITIES = "code_vulnerabilities"
    MAINTENANCE = "maintenance"
    CONTINUOUS_TESTING = "continuous_testing"
    SOURCE_RISK_ASSESSMENT = "source_risk_assessment"
    BUILD_RISK_ASSESSMENT = "build_risk_assessment"


class UserRequirements:
    """
    Represents the weights/priorities of the OpenSSF Scorecard
    check categories.

    Attributes:
        source_risk_assessment (int): The risk assessment of the source.
        maintenance (int): The maintenance of the project.
        build_risk_assessment (int): The risk assessment of the build.
        continuous_testing (int): The continuous testing of the project.
        code_vulnerabilities (int): The code vulnerabilities of the project.
    """
    code_vulnerabilities: int = 10
    maintenance: int = 10
    continuous_testing: int = 10
    source_risk_assessment: int = 10
    build_risk_assessment: int = 10

    def __init__(self, requirements: dict[str, int]):
        """
        Initializes the user requirements.
        
        Args:
            requirements (dict): The user requirements.
        """
        self.code_vulnerabilities = requirements.get(
            RequirementsType.CODE_VULNERABILITIES, 10)
        self.maintenance = requirements.get(
            RequirementsType.MAINTENANCE, 10)
        self.continuous_testing = requirements.get(
            RequirementsType.CONTINUOUS_TESTING, 10)
        self.source_risk_assessment = requirements.get(
            RequirementsType.SOURCE_RISK_ASSESSMENT, 10)
        self.maintenance = requirements.get(
            RequirementsType.MAINTENANCE, 10)
        self.build_risk_assessment = requirements.get(
            RequirementsType.BUILD_RISK_ASSESSMENT, 10)

        self.validate()

    def validate(self):
        """
        Validate the user requirements.

        Raises:
            ValueError: If the user requirements are invalid.
        """
        def is_int(value) -> bool:
            return not isinstance(value, bool) and isinstance(value, int)

        if not (is_int(self.source_risk_assessment) and
                is_int(self.maintenance) and
                is_int(self.build_risk_assessment) and
                is_int(self.continuous_testing) and
                is_int(self.code_vulnerabilities)):
            raise TypeError("input arguments are not integers")

        if not (0 <= self.source_risk_assessment <= 10 and
                0 <= self.maintenance <= 10 and
                0 <= self.build_risk_assessment <= 10 and
                0 <= self.continuous_testing <= 10 and
                0 <= self.code_vulnerabilities <= 10):
            raise ValueError(
                "input arguments fall out of bounds,\
                check if input variables are within the bounds 0 to 10")
