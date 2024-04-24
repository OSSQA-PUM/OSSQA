"""
This module tests the functionality of analyzing an SBOM.
"""
import pytest
import requests

HOST = "http://localhost:5091"


@pytest.fixture(name="scored_sbom_dict", scope="function")
def scored_sbom_dict_fixture() -> dict:
    """
    This fixture creates the dict of an SBOM with scores.
    The dict is formatted according to Sbom.to_dict().
    """
    # TODO: create a scored SBOM
    return {}


@pytest.fixture(autouse=True, scope="function")
def check_sbom_existance():
    """
    This fixture checks whether each test has resulted in an added SBOM
    in the backend database.
    """
    resp = requests.post(HOST + "/test/reset", timeout=10)
    assert resp.status_code == 200

    resp = requests.get(HOST + "/sbom", timeout=10)
    assert resp.status_code == 200
    assert len(resp.json()) == 0

    yield

    resp = requests.get(HOST + "/sbom", timeout=10)
    assert resp.status_code == 200
    assert len(resp.json()) != 0


@pytest.mark.order(-1) # Ensures the tests run after all unit tests
class TestAnalyzeSBOM:
    def test_backend(self, sbom_dict: dict):
        resp = requests.post(HOST + "/sbom", json=sbom_dict, timeout=10)
        assert resp.status_code == 201

    def test_backend_comm(self):
        pass
