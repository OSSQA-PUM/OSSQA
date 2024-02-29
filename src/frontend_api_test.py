import frontend_api

frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                source_risk_assessment = 2,\
                maintence = 1,\
                continuous_testing = 1, code_vunerabilities = 1)

def test():
    """
    Integer Value Testing:

        - Testing valid and invalid integer priority values. 
    """
    x = 0
    for i in range(-1, 12):
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = i,\
                    source_risk_assessment = 1,\
                    maintence = 1,\
                    continuous_testing = 1, code_vunerabilities = 1)
        except:
            if (0 <= i <= 10):
                x = 100
            x += 1
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                    source_risk_assessment = i,\
                    maintence = 1,\
                    continuous_testing = 1, code_vunerabilities = 1)
        except:
            if (0 <= i <= 10):
                x = 100
            x += 1
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                    source_risk_assessment = 1,\
                    maintence = i,\
                    continuous_testing = 1, code_vunerabilities = 1)
        except:
            if (0 <= i <= 10):
                x = 100
            x += 1
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                    source_risk_assessment = 1,\
                    maintence = 1,\
                    continuous_testing = i, code_vunerabilities = 1)
        except:
            if (0 <= i <= 10):
                x = 100
            x += 1
        try:
            frontend_api.frontend_api(path = "src/prototype/example-SBOM.json",  build_risk_assessment = 1,\
                    source_risk_assessment = 1,\
                    maintence = 1,\
                    continuous_testing = 1, code_vunerabilities = i)
        except:
            if (0 <= i <= 10):
                x = 100
            x += 1
    if (x == 10):
        print("Integer Value Testing PASSED \n")

    # TODO
    """
    Decimal value testing.

        - Testing for valid and invalid decimal priority values
    """

    # TODO
    """
    SBOM testing:

        - Testing for valid and invalid SBOMs
    """

test()