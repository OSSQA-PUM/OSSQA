import sys

import pytest
from unittest.mock import patch

from main.frontend.cli import ossqa_cli

from tests.main.integration.constants import HOST


# TODO: populate database with an SBOM before these tests
@pytest.mark.order(-1) # Ensures the tests run after all unit tests
class TestGetSbomNames:
    """
    These functions test the action of getting SBOM names from the
    database in a bottom-up fashion.
    """

    def test_backend(self):
        pass

    def test_backend_comm(self):
        pass

    def test_sbom_processor(self):
        pass

    def test_front_end_api(self):
        pass

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