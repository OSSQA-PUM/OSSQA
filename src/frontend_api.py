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
    return


def check_format_of_sbom(sbom_string):
    """
    Checks that the inputed SBOM meets the standard
    requirement of CycloneDX
    """
    if not sbom_string["bomFormat"] == "CycloneDX":
        raise SyntaxError("bomFormat missing or not CycloneDX")
    if not sbom_string["specVersion"] in ["1.2","1.3","1.4","1.5"]:
        raise ValueError("CycloneDX version missing, out of date or incorrect")
    if not match("^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", sbom_string["serialNumber"]):
        raise SyntaxError("SBOM Serial number does not match the RFC-4122 format")
    if not sbom_string["version"] >= 1:
        raise ValueError("Version of SBOM is lower than 1")
    if not isinstance(sbom_string["version"], int):
        raise ValueError("Version of SBOM is not proper integer")
    return True


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
    #print(path, source_risk_assessment,\
    #                maintence, build_risk_assessment,\
    #                continuous_testing, code_vunerabilities)
    #return main_application_structure()


# End-of-file (EOF)
