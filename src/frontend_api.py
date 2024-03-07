"""
Created: 27/2-2024
Last Edit: 05/03-2024
This file contains the API that communicates information
 from the commandline interface or webinterface to the main 
 application structure
"""

#import main_application_structure
import json

from re import match
from mas import analyze_sbom
from util import UserRequirements

def check_input_arguments(requirements: UserRequirements) -> None:
    """
    Checks wheter the arguments that weight the-
    dependencies fall within the bounds 0 to 10,
    raises ValueError if not.
    """
    requirements.validate()

def check_format_of_sbom(sbom_file) -> None:
    """
    Checks that the inputed SBOM meets the standard
    requirement of CycloneDX
    """
    if not sbom_file["bomFormat"] == "CycloneDX":
        raise SyntaxError("bomFormat missing or not CycloneDX")

    if not sbom_file["specVersion"] in ["1.2","1.3","1.4","1.5"]:
        raise IndexError("CycloneDX version missing, out of date or incorrect")

    if not match(
        "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"+
        "[0-9a-f]{4}-[0-9a-f]{12}$",
        sbom_file["serialNumber"]):
        raise SyntaxError(
            "SBOM Serial number does not match the RFC-4122 format")

    if not sbom_file["version"] >= 1:
        raise IndexError("Version of SBOM is lower than 1")

    if not isinstance(sbom_file["version"], int):
        raise IndexError("Version of SBOM is not proper integer")

    # Checks if name of SBOM exists
    try:
        name = sbom_file["metadata"]["tools"][0]["name"]
    except (IndexError, KeyError):
        name = ""

    if name == "":
        raise ValueError("Name could not be found, non valid SBOM")

def frontend_api(path, user_requirements: UserRequirements = None) -> list[float]:
    """
    This function is called by either frontend interfaces,
    it takes the a file-path to a generated SBOM and desired
    priority of security categories
    and returns a list of weighted scores,
    security categories are defaulted to 10 if no value is
    given since that would equal a weight of 100%
    """
    if not user_requirements:
        user_requirements = UserRequirements()

    check_input_arguments(user_requirements)

    with open(path, encoding="utf-8") as sbom_file:
        sbom_dict = json.load(sbom_file)
        check_format_of_sbom(sbom_dict)
        return analyze_sbom(sbom_dict, requirements=user_requirements)
# End-of-file (EOF)
