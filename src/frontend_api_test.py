"""
Import file with code to be examined
"""
import frontend_api

#frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
#                source_risk_assessment = 2,\
#                maintence = 1,\
#                continuous_testing = 1, code_vunerabilities = 1)

def test():
    """
    Testing Function:

        - Valid SBOM Testing
        - Integer Value Testing
        - Decimal Value Testing
    """
    # Valid SBOM Testing
    if valid_sbom_testing():
        print("\nValid SBOM Testing PASSED \n")
    else:
        print("\nValid SBOM Testing FAILED \n")
    # Integer Value Testing
    if integer_value_testing():
        print("Integer Value Testing PASSED \n")
    else:
        print("Integer Value Testing FAILED \n")
    # Decimal Value Testing
    if decimal_value_testing():
        print("Decimal Value Testing PASSED \n")
    else:
        print("Decimal Value Testing FAILED \n")
        

def integer_value_testing() -> bool:
    """
    Integer Value Testing:

        - Testing valid and invalid integer priority values.
    """
    result = True
    total_errors = 0
    for i in range(-10, 101):
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
            total_errors += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
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
            total_errors += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
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
            total_errors += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
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
            total_errors += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
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
            total_errors += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
    return result and total_errors == 500

def decimal_value_testing() -> bool:
    """
    Decimal Value Testing:

        - Testing decimal priority values
    """
    i = -10
    decimal_number_count = 0
    neg_int_count = 0
    result = True
    while i <= 10:
        x = round(i, 1)
        i += 0.1
        i = round(i,1)
        if i == int(i):
            i = int(i) # Because I don't want to check whole numbers here
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = x)
        except ValueError:
            if x >= 0 and isinstance(x, int):
                result = False
            elif x != int(x):
                decimal_number_count += 1
            elif x == int(x) and x < 0:
                neg_int_count += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = x,\
                                      code_vunerabilities = 1)
        except ValueError:
            if x >= 0 and isinstance(x, int):
                result = False
            elif x != int(x):
                decimal_number_count += 1
            elif x == int(x) and x < 0:
                neg_int_count += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = x,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if x >= 0 and isinstance(x, int):
                result = False
            elif x != int(x):
                decimal_number_count += 1
            elif x == int(x) and x < 0:
                neg_int_count += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = x,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if x >= 0 and isinstance(x, int):
                result = False
            elif x != int(x):
                decimal_number_count += 1
            elif x == int(x) and x < 0:
                neg_int_count += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = x,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
        except ValueError:
            if x >= 0 and isinstance(x, int):
                result = False
            elif x != int(x):
                decimal_number_count += 1
            elif x == int(x) and x < 0:
                neg_int_count += 1
        except IndexError:
            continue
        except SyntaxError:
            continue
    return result and decimal_number_count == 900 and neg_int_count == 50

def valid_sbom_testing() -> bool:
    """
    Valid SBOM Testing:

        - Testing if correct format of SBOM
        - Testing if valid specVersion
        - Testing if valid serial number
    """
    # Testing if correct format of SBOM
    result = True
    try:
        frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
    except SyntaxError:
        result = False
    except IndexError:
        result = False
    return result

test()

# End-of-file (EOF)