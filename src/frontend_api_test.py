"""
Import file with code to be examined
"""
import frontend_api

frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                source_risk_assessment = 2,\
                maintence = 1,\
                continuous_testing = 1, code_vunerabilities = 1)

def test():
    """
    Testing Function:

        - Integer Value Testing
        - Decimal Value Testing
        - Valid SBOM Testing
    """
    # Integer Value Testing
    if integer_value_testing():
        print("\nInteger Value Testing PASSED \n")
    else:
        print("\nInteger Value Testing FAILED \n")
    # Decimal Value Testing
    if decimal_value_testing():
        print("Decimal Value Testing PASSED \n")
    else:
        print("Decimal Value Testing FAILED \n")
    # Valid SBOM Testing
    if valid_sbom_testing():
        print("Valid SBOM Testing PASSED \n")
    else:
        print("Valid SBOM Testing FAILED \n")
        

def integer_value_testing() -> bool:
    """
    Integer Value Testing:

        - Testing valid and invalid integer priority values.
    """
    result = True
    for i in range(-10, 100):
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = i,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if 0 <= i <= 10:
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = i,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if 0 <= i <= 10:
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = i,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if 0 <= i <= 10:
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = i,\
                                      code_vunerabilities = 1)
        except ValueError:
            if 0 <= i <= 10:
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = i)
        except ValueError:
            if 0 <= i <= 10:
                result = False
    return result

def decimal_value_testing() -> bool:
    """
    Decimal Value Testing:

        - Testing decimal priority values
    """
    i = -10
    result = True
    while i <= 10:
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = i)
        except ValueError:
            if i >= 0 and isinstance(i, int):
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = i,\
                                      code_vunerabilities = 1)
        except ValueError:
            if i >= 0 and isinstance(i, int):
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = i,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if i >= 0 and isinstance(i, int):
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = i,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if i >= 0 and isinstance(i, int):
                result = False
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = i,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if i >= 0 and isinstance(i, int):
                result = False
        i += 0.1
    return result

def valid_sbom_testing() -> bool:
    """
    Valid SBOM Testing:

        - Testing if correct format of SBOM
        - Testing if valid specVersion
        - Testing if valid serial number
    """
    # Testing if correct format of SBOM
    # TODO Write these tests
    return True

test()

# End-of-file (EOF)