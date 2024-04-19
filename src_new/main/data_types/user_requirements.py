"""
This module contains every datatype related to user-specified
requirements.
"""
from enum import StrEnum


class RequirementsEnum(StrEnum):
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

    def __init__(self, requirements: dict):
        """
        Initializes the user requirements.
        
        Args:
            requirements (dict): The user requirements.
        """
        self.code_vulnerabilities = requirements.get(
            RequirementsEnum.CODE_VULNERABILITIES)
        self.maintenance = requirements.get(
            RequirementsEnum.MAINTENANCE)
        self.continuous_testing = requirements.get(
            RequirementsEnum.CONTINUOUS_TESTING)
        self.source_risk_assessment = requirements.get(
            RequirementsEnum.SOURCE_RISK_ASSESSMENT)
        self.maintenance = requirements.get(
            RequirementsEnum.MAINTENANCE)
        self.build_risk_assessment = requirements.get(
            RequirementsEnum.BUILD_RISK_ASSESSMENT)

        self.validate()

    def validate(self):
        """
        Validate the user requirements.

        Raises:
            ValueError: If the user requirements are invalid.
        """
        if not (isinstance(self.source_risk_assessment, int) and
                isinstance(self.maintenance, int) and
                isinstance(self.build_risk_assessment, int) and
                isinstance(self.continuous_testing, int) and
                isinstance(self.code_vulnerabilities, int)):
            raise TypeError("input arguments are not integers")

        if not (0 <= self.source_risk_assessment <= 10 and
                0 <= self.maintenance <= 10 and
                0 <= self.build_risk_assessment <= 10 and
                0 <= self.continuous_testing <= 10 and
                0 <= self.code_vulnerabilities <= 10):
            raise ValueError(
                "input arguments fall out of bounds,\
                check if input variables are within the bounds 0 to 10")
