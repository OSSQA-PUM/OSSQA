"""
This module tests the functionality of analyzing an SBOM.
"""
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
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import (RequirementsType,
                                               UserRequirements)

from tests.main.integration.constants import HOST
from tests.main.integration.sboms import SBOM_PATH, create_scored_sbom, \
    create_unscored_sbom


@pytest.fixture(name="git_token", scope="module")
def git_token_fixture() -> str:
    return os.environ.get("GITHUB_AUTH_TOKEN", "invalid_token")


@pytest.fixture(name="user_reqs", scope="module")
def user_reqs_fixture() -> UserRequirements:
    req_types = [t.value for t in RequirementsType]
    reqs_dict = {req_type: 10 for req_type in req_types}
    return UserRequirements(reqs_dict)


@pytest.fixture(name="sbom_path", scope="module")
def sbom_path_fixture() -> Path:
    return SBOM_PATH


@pytest.fixture(name="sbom", scope="function")
def sbom_fixture(sbom_path: Path) -> Sbom:
    """
    This fixture reads an SBOM file and creates an Sbom object.
    """
    return create_unscored_sbom()


@pytest.fixture(name="fake_scored_sbom", scope="function")
def fake_scored_sbom_fixture(sbom_path: Path) -> Sbom:
    """
    This fixture reads and SBOM file and creates an Sbom object
    with fake scorecard data.
    """
    return create_scored_sbom()


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


@pytest.mark.order(-3)  # Ensures the tests run after all unit tests
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

        scored_deps = res_sbom.get_scored_dependencies()
        assert len(scored_deps) != 0
        after_test()

    def test_front_end_api(self, sbom: Sbom, user_reqs: UserRequirements):
        before_test()
        front_end_api = FrontEndAPI(HOST)
        res_sbom = front_end_api.analyze_sbom(sbom, user_reqs)

        scored_deps = res_sbom.get_scored_dependencies()
        assert len(scored_deps) != 0
        after_test()

    def test_cli(self, sbom_path: Path, git_token: str):
        before_test()

        # Temporarily overwrite sys.argv, then run the CLI
        # TODO: add user requirements to mock_args
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
