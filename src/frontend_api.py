"""
Created: 27/2-2024
Last Edit: 27/2-2024
This file contains the API that communicates information
 from the commandline interface or webinterface to the main 
 application structure
"""
import os
#import sys

#import main_application_structure
import json
from io import StringIO


def check_input_arguments(path, source_risk_assessment,\
                    maintence, build_risk_assessment,\
                    continuous_testing, code_vunerabilities):
    """
    Checks wheter the arguments that weight the-
    dependencies fall within the bounds 0 to 10,
    raises ValueError if not.
    """
    if not (0 <= source_risk_assessment <= 10 or \
                0 <= maintence <=10 or 0 <= build_risk_assessment <= 10 or \
                0 <= continuous_testing <= 10 or 0 <= code_vunerabilities <= 10):
        raise ValueError("input arguments fall out of bounds, check if input variables are within the bounds 0 to 10",\
                                [source_risk_assessment, maintence,\
                                build_risk_assessment, continuous_testing,\
                                code_vunerabilities])
    return


def check_format_of_sbom(TBD):
    """
    Checks that the inputed SBOM meets the standard
    requirement of CycloneDX
    """
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
    print(os.getcwd())
    check_input_arguments(path, source_risk_assessment, maintence, 
                              build_risk_assessment, continuous_testing,
                              code_vunerabilities)
    
    #print(open(path, encoding="utf-8"))
    #with open(path, encoding="utf-8") as file:
    sbom_json = open(path, encoding="utf-8")
    sbom_string = json.load(sbom_json)
    #print(sbom)
       
    print(path, source_risk_assessment,\
                    maintence, build_risk_assessment,\
                    continuous_testing, code_vunerabilities)
    #return main_application_structure()


frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1, source_risk_assessment = 1,\
                    maintence = 1,\
                    continuous_testing = 1, code_vunerabilities = 10)





# End-of-file (EOF)
