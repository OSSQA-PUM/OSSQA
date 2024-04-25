"""
This module tests the functionality of analyzing an SBOM.
"""
import json

import pytest
import requests

from main.backend_communication import BackendCommunication
from main.data_types.dependency_scorer import StepResponse
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.scorecard import Scorecard

from tests.main.unit.sboms.sboms import PATHS as SBOM_PATHS
from tests.main.unit.scorecards.scorecards import PATHS as SCORECARD_PATHS

HOST = "http://localhost:5091"


@pytest.fixture(name="sbom", scope="module")
def sbom_fixture() -> Sbom:
    """
    This fixture reads an SBOM file and creates an Sbom object.
    """
    with open(SBOM_PATHS[0], "r", encoding="utf-8") as sbom_file:
        return Sbom(json.load(sbom_file))


@pytest.fixture(name="fake_scored_sbom", scope="module")
def fake_scored_sbom_fixture() -> Sbom:
    """
    This fixture reads and SBOM file and creates an Sbom object
    with fake scorecard data.
    """
    with open(SBOM_PATHS[0], "r", encoding="utf-8") as sbom_file:
        sbom = Sbom(json.load(sbom_file))

    unscored_deps = sbom.dependency_manager.get_unscored_dependencies()
    max_idx = min(len(unscored_deps), len(SCORECARD_PATHS))
    scored_deps = []

    for idx in range(max_idx):
        with open(SCORECARD_PATHS[idx], "r", encoding="utf-8") as file:
            scorecard = Scorecard(json.load(file))
        dependency = unscored_deps[idx]
        dependency.dependency_score = scorecard
        scored_deps.append(dependency)

    sbom.dependency_manager.update(scored_deps)
    return sbom


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
    """
    These functions test the action of analyzing an SBOM.
    """

    def test_backend(self, fake_scored_sbom: Sbom):
        sbom_dict = fake_scored_sbom.to_dict()
        resp = requests.post(HOST + "/sbom", json=sbom_dict, timeout=10)
        assert resp.status_code == 201

    @pytest.mark.skip("The HOST BackendCommunication uses only works in docker")
    @pytest.mark.asyncio
    async def test_backend_comm(self, fake_scored_sbom: Sbom):
        def callback(response: StepResponse):
            assert response.message != "The request timed out"
        backend_comm = BackendCommunication(callback)
        await backend_comm.add_sbom(fake_scored_sbom)
