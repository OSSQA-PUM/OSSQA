"""
This module tests the functionality of gettings SBOMs with specific names
from the database.
"""
import pytest


@pytest.mark.order(-1) # Ensures the tests run after all unit tests
class TestGetNamedSboms:
    """
    These functions test the action of getting SBOMs with specific names
    from the database in a bottom-up fashion.
    """