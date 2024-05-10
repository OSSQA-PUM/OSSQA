"""
This module tests the functionality of analyzing an SBOM.
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from main.backend_communication import BackendCommunication
from main.frontend.cli import ossqa_cli
from main.frontend.front_end_api import FrontEndAPI
from main.sbom_processor import SbomProcessor
from main.data_types.dependency_scorer import StepResponse
from main.data_types.user_requirements import RequirementsType, UserRequirements
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.scorecard import Scorecard

from tests.main.integration.constants import HOST
from tests.main.unit.sboms.sboms import PATHS as SBOM_PATHS
from tests.main.unit.scorecards.scorecards import PATHS as SCORECARD_PATHS


@pytest.fixture(name="git_token", scope="module")
def git_token_fixture() -> str:
    return os.environ.get("GITHUB_AUTH_TOKEN", "invalid_token")


@pytest.fixture(name="user_reqs", scope="module")
def user_reqs_fixture() -> UserRequirements:
    req_types = [t.value for t in RequirementsType]
    reqs_dict = {req_type:10 for req_type in req_types}
    return UserRequirements(reqs_dict)


@pytest.fixture(name="sbom_path", scope="module")
def sbom_path_fixture() -> Path:
    return SBOM_PATHS[0]


@pytest.fixture(name="sbom", scope="module")
def sbom_fixture(sbom_path: Path) -> Sbom:
    """
    This fixture reads an SBOM file and creates an Sbom object.
    """
    with open(sbom_path, "r", encoding="utf-8") as sbom_file:
        return Sbom(json.load(sbom_file))


@pytest.fixture(name="fake_scored_sbom", scope="module")
def fake_scored_sbom_fixture(sbom_path: Path) -> Sbom:
    """
    This fixture reads and SBOM file and creates an Sbom object
    with fake scorecard data.
    """
    with open(sbom_path, "r", encoding="utf-8") as sbom_file:
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


def before_test():
    """
    Resets the backend database and checks that the reset is successful.
    """
    resp = requests.post(HOST + "/test/reset", timeout=10)
    assert resp.status_code == 200
    resp = requests.get(HOST + "/sbom", timeout=10)
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def after_test():
    """
    Checks that an SBOM has been successfully added to the backend database.
    """
    resp = requests.get(HOST + "/sbom", timeout=10)
    assert resp.status_code == 200
    assert len(resp.json()) != 0


@pytest.mark.order(-2) # Ensures the tests run after all unit tests
class TestAnalyzeSBOM:
    """
    These functions test the action of analyzing an SBOM in a
    bottom-up fashion.
    """

    def test_backend(self, fake_scored_sbom: Sbom):
        before_test()
        sbom_dict = fake_scored_sbom.to_dict()
        resp = requests.post(HOST + "/sbom", json=sbom_dict, timeout=10)
        assert resp.status_code == 201
        after_test()

    def test_backend_comm(self, fake_scored_sbom: Sbom):
        before_test()
        def callback(response: StepResponse):
            assert response.message != "The request timed out"
        backend_comm = BackendCommunication(callback, HOST)
        backend_comm.add_sbom(fake_scored_sbom)
        after_test()

    def test_sbom_processor(self, sbom: Sbom):
        before_test()
        sbom_proc = SbomProcessor(HOST)
        res_sbom = sbom_proc.analyze_sbom(sbom)

        unscored_deps = res_sbom.dependency_manager.get_unscored_dependencies()
        scored_deps = res_sbom.dependency_manager.get_scored_dependencies()
        assert len(unscored_deps) == 0
        print(scored_deps)
        assert len(scored_deps) == 0
        after_test()

    def test_front_end_api(self, sbom: Sbom, user_reqs: UserRequirements):
        before_test()
        front_end_api = FrontEndAPI(HOST)
        res_sbom = front_end_api.analyze_sbom(sbom, user_reqs)

        unscored_deps = res_sbom.dependency_manager.get_unscored_dependencies()
        scored_deps = res_sbom.dependency_manager.get_scored_dependencies()
        assert len(unscored_deps) == 0
        print(scored_deps)
        assert len(scored_deps) == 0
        after_test()

    def test_cli(self, sbom_path: Path, git_token: str):
        before_test()

        # Temporarily overwrite sys.argv, then run the CLI
        mock_args = [
            "prog",
            "analyze",
            "-g", git_token,
            "--backend", HOST,
            str(sbom_path),
        ]
        with patch("sys.argv", mock_args):
            assert sys.argv == mock_args
            try:
                ossqa_cli()
            except SystemExit as e:
                # Click explicitly calls sys.exit, so this needs to be caught
                assert e.code == 0

        after_test()
