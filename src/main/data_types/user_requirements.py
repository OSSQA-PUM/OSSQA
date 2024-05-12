"""
This module contains every datatype related to user-specified
requirements.
"""
from enum import StrEnum


class RequirementsType(StrEnum):
    """
    Mappings between strings and OpenSSF Scorecard tests.
    """
    VULNERABILITIES = "vulnerabilities"
    DEPENDENCY_UPDATE_TOOL = "dependency_update_tool"
    MAINTAINED = "maintained"
    SECURITY_POLICY = "security_policy"
    LICENSE = "license"
    CII_BEST_PRACTICES = "cii_best_practices"
    CI_TESTS = "ci_tests"
    FUZZING = "fuzzing"
    SAST = "sast"
    BINARY_ARTIFACTS = "binary_artifacts"
    BRANCH_PROTECTION = "branch_protection"
    DANGEROUS_WORKFLOW = "dangerous_workflow"
    CODE_REVIEW = "code_review"
    CONTRIBUTORS = "contributors"
    PINNED_DEPENDENCIES = "pinned_dependencies"
    TOKEN_PERMISSIONS = "token_permissions"
    PACKAGING = "packaging"
    SIGNED_RELEASES = "signed_releases"


class UserRequirements:
    """
    Represents the weights/priorities of the OpenSSF Scorecard
    tests.
    Attributes:
        source_risk_assessment (int): The risk assessment of the source.
        includes:
            vulnerabilities (int): The vulnerabilities of the project.
        maintenance (int): The maintenance of the project.
        includes:
            dependency_update_tool (int): The dependency update tool of the project.
            maintained (int): The maintenance of the project.
            security_policy (int): The security policy of the project.
            license (int): The license of the project.
            cii_best_practices (int): The CII best practices of the project.
        build_risk_assessment (int): The risk assessment of the build.
        includes:
            ci_tests (int): The CI tests of the project.
            fuzzing (int): The fuzzing of the project.
            sast (int): The SAST of the project.
        continuous_testing (int): The continuous testing of the project.
        includes:
            binary_artifacts (int): The binary artifacts of the project.
            branch_protection (int): The branch protection of the project.
            dangerous_workflow (int): The dangerous workflow of the project.
            code_review (int): The code review of the project.
            contributors (int): The contributors of the project.
        code_vulnerabilities (int): The code vulnerabilities of the project.
        includes:
            pinned_dependencies (int): The pinned dependencies of the project.
            token_permissions (int): The token permissions of the project.
            packaging (int): The packaging of the project.
            signed_releases (int): The signed releases of the project.
    """
    vulnerabilities: int = -1
    dependency_update_tool: int = -1
    maintained: int = -1
    security_policy: int = -1
    license: int = -1
    cii_best_practices: int = -1
    ci_tests: int = -1
    fuzzing: int = -1
    sast: int = -1
    binary_artifacts: int = -1
    branch_protection: int = -1
    dangerous_workflow: int = -1
    code_review: int = -1
    contributors: int = -1
    pinned_dependencies: int = -1
    token_permissions: int = -1
    packaging: int = -1
    signed_releases: int = -1

    def __init__(self, requirements: dict[str, int]):
        """
        Initializes the user requirements.

        Args:
            requirements (dict): The user requirements.
        """
        self.code_vulnerabilities = requirements.get(
            RequirementsType.VULNERABILITIES, -1)
        self.dependency_update_tool = requirements.get(
            RequirementsType.DEPENDENCY_UPDATE_TOOL, -1)
        self.maintained = requirements.get(
            RequirementsType.MAINTAINED, -1)
        self.security_policy = requirements.get(
            RequirementsType.SECURITY_POLICY, -1)
        self.license = requirements.get(
            RequirementsType.LICENSE, -1)
        self.cii_best_practices = requirements.get(
            RequirementsType.CII_BEST_PRACTICES, -1)
        self.ci_tests = requirements.get(
            RequirementsType.CI_TESTS, -1)
        self.fuzzing = requirements.get(
            RequirementsType.FUZZING, -1)
        self.sast = requirements.get(
            RequirementsType.SAST, -1)
        self.binary_artifacts = requirements.get(
            RequirementsType.BINARY_ARTIFACTS, -1)
        self.branch_protection = requirements.get(
            RequirementsType.BRANCH_PROTECTION, -1)
        self.dangerous_workflow = requirements.get(
            RequirementsType.DANGEROUS_WORKFLOW, -1)
        self.code_review = requirements.get(
            RequirementsType.CODE_REVIEW, -1)
        self.contributors = requirements.get(
            RequirementsType.CONTRIBUTORS, -1)
        self.pinned_dependencies = requirements.get(
            RequirementsType.PINNED_DEPENDENCIES, -1)
        self.token_permissions = requirements.get(
            RequirementsType.TOKEN_PERMISSIONS, -1)
        self.packaging = requirements.get(
            RequirementsType.PACKAGING, -1)
        self.signed_releases = requirements.get(
            RequirementsType.SIGNED_RELEASES, -1)

        self.validate()

    def validate(self):
        """
        Validate the user requirements.

        Raises:
            ValueError: If the user requirements are invalid.
        """
        def is_int(value) -> bool:
            return not isinstance(value, bool) and isinstance(value, int)
        for attr in self.__dict__:
            if not is_int(getattr(self, attr)):
                print(f"Invalid value for {attr}")
        if not (is_int(self.vulnerabilities) and
                is_int(self.dependency_update_tool) and
                is_int(self.maintained) and
                is_int(self.security_policy) and
                is_int(self.license) and
                is_int(self.cii_best_practices) and
                is_int(self.ci_tests) and
                is_int(self.fuzzing) and
                is_int(self.sast) and
                is_int(self.binary_artifacts) and
                is_int(self.branch_protection) and
                is_int(self.dangerous_workflow) and
                is_int(self.code_review) and
                is_int(self.contributors) and
                is_int(self.pinned_dependencies) and
                is_int(self.token_permissions) and
                is_int(self.packaging) and
                is_int(self.signed_releases)):
            raise TypeError("input arguments are not integers")

        if not (-1 <= self.vulnerabilities <= 10 and
                -1 <= self.dependency_update_tool <= 10 and
                -1 <= self.maintained <= 10 and
                -1 <= self.security_policy <= 10 and
                -1 <= self.license <= 10 and
                -1 <= self.cii_best_practices <= 10 and
                -1 <= self.ci_tests <= 10 and
                -1 <= self.fuzzing <= 10 and
                -1 <= self.sast <= 10 and
                -1 <= self.binary_artifacts <= 10 and
                -1 <= self.branch_protection <= 10 and
                -1 <= self.dangerous_workflow <= 10 and
                -1 <= self.code_review <= 10 and
                -1 <= self.contributors <= 10 and
                -1 <= self.pinned_dependencies <= 10 and
                -1 <= self.token_permissions <= 10 and
                -1 <= self.packaging <= 10 and
                -1 <= self.signed_releases <= 10):
            raise ValueError(
                "input arguments fall out of bounds,\
                check if input variables are within the bounds 0 to 10")

    def get_listed_requirements(self) -> list[str]:
        """
        Get a list of the requirements.
        Returns:
            list[str]: The list of requirements.
        """
        return [["Vulnerabilities", self.vulnerabilities],["Dependency-Update-Tool", self.dependency_update_tool],
                ["Maintained", self.maintained],["Security-Policy", self.security_policy],
                ["License", self.license],["CII-Best-Practices", self.cii_best_practices],
                ["CI-Tests", self.ci_tests],["Fuzzing", self.fuzzing],["SAST", self.sast],
                ["Binary-Artifacts", self.binary_artifacts],["Branch-Protection", self.branch_protection],
                ["Dangerous-Workflow", self.dangerous_workflow],["Code-Review", self.code_review],
                ["Contributors", self.contributors],["Pinned-Dependencies", self.pinned_dependencies],
                ["Token-Permissions", self.token_permissions],["Packaging", self.packaging],
                ["Signed-Releases", self.signed_releases]]

    def to_dict(self) -> dict:
        """
        Get a dictionary of the requirements.
        Returns:
            dict: The dictionary of requirements.
        """
        return {
            "Vulnerabilities": self.vulnerabilities,
            "Dependency-Update-Tool": self.dependency_update_tool,
            "Maintained": self.maintained,
            "Security-Policy": self.security_policy,
            "License": self.license,
            "CII-Best-Practices": self.cii_best_practices,
            "CI-Tests": self.ci_tests,
            "Fuzzing": self.fuzzing,
            "SAST": self.sast,
            "Binary-Artifacts": self.binary_artifacts,
            "Branch-Protection": self.branch_protection,
            "Dangerous-Workflow": self.dangerous_workflow,
            "Code-Review": self.code_review,
            "Contributors": self.contributors,
            "Pinned-Dependencies": self.pinned_dependencies,
            "Token-Permissions": self.token_permissions,
            "Packaging": self.packaging,
            "Signed-Releases": self.signed_releases
        }