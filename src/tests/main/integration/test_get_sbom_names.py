import pytest

from tests.main.integration.constants import HOST


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
        pass