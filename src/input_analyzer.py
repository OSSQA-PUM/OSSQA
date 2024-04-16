"""
Created: 27/2-2024
Last Edit: 07/03-2024
This file contains the API that communicates information
 from the commandline interface or webinterface to the main 
 application structure
"""
import json

from re import match
from util import UserRequirements
import calculate_dependencies


def check_input_arguments(requirements: UserRequirements) -> None:
    """
    Check if the input arguments meet the specified requirements.

    Args:
        requirements (UserRequirements): The user requirements object.

    Returns:
        None
    """
    try:
        requirements.validate()
    except ValueError as e:
        raise ValueError("Input arguments are invalid") from e
    except TypeError as e:
        raise TypeError("Input arguments are not integers") from e


def check_format_of_sbom(sbom_file) -> None:
    """
    Checks the format of the SBOM file.

    Args:
        sbom_file (dict): The SBOM file to be checked.

    Raises:
        SyntaxError: If the 'bomFormat' is missing or not 'CycloneDX'.

        IndexError: If the 'specVersion' is missing, out of date, or incorrect.

        SyntaxError: If the 'serialNumber' does not match the RFC-4122 format.

        IndexError: If the 'version' of SBOM is lower than 1
        or not a proper integer.

        ValueError: If the name could not be found, indicating a non-valid SBOM.
    """
    if not sbom_file["bomFormat"] == "CycloneDX":
        raise SyntaxError("bomFormat missing or not CycloneDX")

    if not sbom_file["specVersion"] in ["1.2", "1.3", "1.4", "1.5"]:
        raise IndexError("CycloneDX version missing, out of date or incorrect")

    if not match(
            "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-" +
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


def get_updates() -> str:
    """
    Get the current status of the analysis. Will be deleted and replaced by observer before final release
    """
    return calculate_dependencies.get_current_status()


def validate_input(sbom_dict, requirements: UserRequirements = None) -> bool:

    check_input_arguments(requirements)

    check_format_of_sbom(sbom_dict)
    return True

# End-of-file (EOF)
