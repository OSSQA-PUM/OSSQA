import pytest

@pytest.fixture(name="flask")
def flask_fixture():
    pass

@pytest.fixture(name="sbom")
def sbom_fixture():
    with open(f"{parametrizied_var}.json", "r") as file:
        return json.load(file)

@pytest.mark.parametrize("var", [sbom, ])
def test_asd(flask, var):
    pass






"""
Fixture functions can be parametrized in which case they will be called multiple times,
 each time executing the set of dependent tests, i. e. the tests that depend on this fixture.
"""

@pytest.fixture(params=["file/path/some.json", "file/path/another.json"])
def sbom_json(request: FixtureRequest):
    with open(request.param, "r") as file:
        return json.load(file)

def test(sbom_json): 
    assert Sbom(sbom_json)   
    pass