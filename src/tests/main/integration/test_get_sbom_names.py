"""
This module tests the functionality of getting SBOM names from the database.
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from main.backend_communication import BackendCommunication
from main.data_types.dependency_scorer import StepResponse
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.scorecard import Scorecard
from main.frontend.cli import ossqa_cli
from main.frontend.front_end_api import FrontEndAPI
from main.sbom_processor import SbomProcessor, SbomProcessorStatus

from tests.main.integration.constants import HOST
from tests.main.integration.sboms import create_scored_sbom


@pytest.fixture(name="fake_scored_sbom", scope="module")
def fake_scored_sbom_fixture() -> Sbom:
    """
    This fixture reads and SBOM file and creates an Sbom object
    with fake scorecard data.
    """
    return create_scored_sbom()


@pytest.mark.order(-2) # Ensures the tests run after all unit tests
class TestGetSbomNames:
    """
    These functions test the action of getting SBOM names from the
    database in a bottom-up fashion.
    """
    def test_populate_database(self, fake_scored_sbom: Sbom):
        resp = requests.post(HOST + "/test/reset", timeout=10)
        assert resp.status_code == 200
        sbom_dict = fake_scored_sbom.to_dict()
        resp = requests.post(HOST + "/sbom", json=sbom_dict, timeout=10)
        assert resp.status_code == 201

    def test_backend(self):
        resp = requests.get(HOST + "/sbom", timeout=5)
        assert resp.status_code == 200
        assert len(resp.json()) != 0

    def test_backend_comm(self):
        def callback(response: StepResponse):
            assert response.message != "The request timed out"
            assert response.message != "An error occurred in the database"
        backend_comm = BackendCommunication(callback, HOST)
        names = backend_comm.get_sbom_names()
        assert isinstance(names, list)
        assert len(names) != 0

    def test_sbom_processor(self):
        def callback(status: SbomProcessorStatus):
            if response := status.step_response:
                assert response.message != "The request timed out"
                assert response.message != "An error occurred in the database"
        sbom_proc = SbomProcessor(HOST)
        sbom_proc.on_status_update.subscribe(callback)
        names = sbom_proc.lookup_stored_sboms()
        assert isinstance(names, list)
        assert len(names) != 0

    def test_front_end_api(self):
        def callback(status: SbomProcessorStatus):
            if response := status.step_response:
                assert response.message != "The request timed out"
                assert response.message != "An error occurred in the database"
        front_end_api = FrontEndAPI(HOST)
        front_end_api.on_sbom_processor_status_update.subscribe(callback)
        names = front_end_api.lookup_stored_sboms()
        assert isinstance(names, list)
        assert len(names) != 0

    def test_cli(self):
        # Temporarily overwrite sys.argv, then run the CLI
        mock_args = ["prog", "sboms", "--backend", HOST]
        with patch("sys.argv", mock_args):
            assert sys.argv == mock_args
            try:
                ossqa_cli()
                # TODO: test this more extensively. maybe catch stdout?
            except SystemExit as e:
                # Click explicitly calls sys.exit, so this needs to be caught
                assert e.code == 0