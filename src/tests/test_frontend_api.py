"""
Import file with code to be examined
"""
import pytest
from frontend_api import frontend_api 

def test_integer_values() -> None:
    """
    Integer Value Testing:

        - Testing valid and invalid integer priority values.
    """
    result = True
    total_errors = 0
    expected_integer_errors = 500
    for i in range(-10, 101):
        try:
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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

    assert result
    assert total_errors == expected_integer_errors

def test_decimal_values() -> None:
    """
    Decimal Value Testing:

        - Testing decimal priority values
    """
    i = -10
    decimal_number_count = 0
    neg_int_count = 0
    result = True
    expected_decimal_errors = 900
    expected_negative_errors = 50
    while i <= 10:
        x = round(i, 1)
        i += 0.1
        i = round(i,1)
        if i == int(i):
            i = int(i) # Because I don't want to check whole numbers here
        try:
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
            frontend_api(path = "src/prototype/example-SBOM.json",\
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
    assert result
    assert decimal_number_count == expected_decimal_errors
    assert neg_int_count == expected_negative_errors

def test_valid_SBOM() -> None:
    """
    Valid SBOM Testing:

        - Testing if correct format of SBOM
        - Testing if valid specVersion
        - Testing if valid serial number
    """
    # Testing if correct format of SBOM
    result = True
    try:
        frontend_api(path = "src/prototype/example-SBOM.json",\
                                      build_risk_assessment = 1,\
                                      source_risk_assessment = 1,\
                                      maintence = 1,\
                                      continuous_testing = 1,\
                                      code_vunerabilities = 1)
    except SyntaxError:
        result = False
    except IndexError:
        result = False
    assert result

# End-of-file (EOF)