"""
Created: 27/2-2024
Last Edit: 27/2-2024
This file contains the API that communicates information
 from the commandline interface or webinterface to the main 
 application structure
"""

#import main_application_structure
import json
from re import match


def check_input_arguments(source_risk_assessment,\
                    maintence, build_risk_assessment,\
                    continuous_testing, code_vunerabilities):
    """
    Checks wheter the arguments that weight the-
    dependencies fall within the bounds 0 to 10,
    raises ValueError if not.
    """
    if not (0 <= source_risk_assessment <= 10 and \
                0 <= maintence <=10 and 0 <= build_risk_assessment <= 10 and \
                0 <= continuous_testing <= 10 and 0 <= code_vunerabilities <= 10):
        raise ValueError("input arguments fall out of bounds, check if input variables are within the bounds 0 to 10",\
                                [source_risk_assessment, maintence,\
                                build_risk_assessment, continuous_testing,\
                                code_vunerabilities])
    if not (isinstance(source_risk_assessment, int) and \
                isinstance(maintence, int) and isinstance(build_risk_assessment, int) and \
                isinstance(continuous_testing, int) and isinstance(code_vunerabilities, int)):
        raise ValueError("input arguments are not integers",\
                                [source_risk_assessment, maintence,\
                                build_risk_assessment, continuous_testing,\
                                code_vunerabilities])
    return


def check_format_of_sbom(sbom_string) -> bool:
    """
    Checks that the inputed SBOM meets the standard
    requirement of CycloneDX
    """
    if not sbom_string["bomFormat"] == "CycloneDX":
        raise SyntaxError("bomFormat missing or not CycloneDX")
    if not sbom_string["specVersion"] in ["1.2","1.3","1.4","1.5"]:
        raise IndexError("CycloneDX version missing, out of date or incorrect")
    if not match("^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", sbom_string["serialNumber"]):
        raise SyntaxError("SBOM Serial number does not match the RFC-4122 format")
    if not sbom_string["version"] >= 1:
        raise IndexError("Version of SBOM is lower than 1")
    if not isinstance(sbom_string["version"], int):
        raise IndexError("Version of SBOM is not proper integer")
    # Checks if name of SBOM exists
    try:
        name = sbom_string["metadata"]["tools"][0]["name"]
    except (IndexError, KeyError):
        name = ""
    if name == "":
        raise ValueError("Name could not be found, non valid SBOM")
    return


def frontend_api(path, source_risk_assessment = 10,\
                    maintence = 10, build_risk_assessment = 10,\
                    continuous_testing = 10, code_vunerabilities = 10):
    """
    This function is called by either frontend interfaces,
    it takes the a file-path to a generated SBOM and desired
    priority of security categories
    and returns a list of weighted scores,
    security categories are defaulted to 10 if no value is
    given since that would equal a weight of 100%
    """
    check_input_arguments(source_risk_assessment, maintence, 
                              build_risk_assessment, continuous_testing,
                              code_vunerabilities)
    
    sbom_json = open(path, encoding="utf-8")
    sbom_string = json.load(sbom_json)
    check_format_of_sbom(sbom_string)
    print(path, source_risk_assessment,\
                    maintence, build_risk_assessment,\
                    continuous_testing, code_vunerabilities)
    return
    #return main_application_structure()

frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 10,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 5,\
                                      code_vunerabilities = 1)

# End-of-file (EOF)
