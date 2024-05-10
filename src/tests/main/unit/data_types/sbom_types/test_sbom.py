"""
This module contains unit tests for the `Sbom` class in the
`sbom` module of the `sbom_types` package.
"""
import json
import pytest
from tests.main.unit.sboms.sboms import (PATHS as SBOM_PATHS,
                                         BAD_SBOMS,
                                         SBOM_COMPONENT_URLS,
                                         DUMMY_DEPENDENCIES)
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.sbom_types.dependency import Dependency


@pytest.fixture(params=SBOM_PATHS)
def sbom_from_json(request):
    """
    Fixture to load an SBOM JSON file.
    """
    with open(request.param, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(params=BAD_SBOMS)
def sbom_bad(request):
    """
    Fixture to load a bad SBOM JSON file.
    """
    return request.param


@pytest.fixture(params=SBOM_COMPONENT_URLS)
def sbom_component_url(request):
    """
    Fixture to load a SBOM component URL.
    """
    return request.param


@pytest.fixture(params=[0, 1, 2, 3])
def sbom_component(request):
    """
    Fixture to load a SBOM component.
    """
    with open(SBOM_PATHS[0], "r", encoding="utf-8") as file:
        sbom_dict = json.load(file)
    return sbom_dict["components"][request.param]


def test_sbom_initialize(sbom_from_json):
    """
    Test that an SBOM can be initialized.
    """
    sbom = Sbom(sbom_from_json)
    assert sbom is not None
    assert isinstance(sbom.serial_number, str)
    assert isinstance(sbom.version, int)
    assert isinstance(sbom.repo_name, str)
    assert isinstance(sbom.repo_version, str)
    assert sbom.dependency_manager is not None


def test_sbom_to_dict(sbom_from_json):
    """
    Test that the to_dict method returns a dictionary representation of the
    SBOM.
    """
    sbom = Sbom(sbom_from_json)
    sbom_dict = sbom.to_dict()
    assert "serialNumber" in sbom_dict.keys()
    assert "version" in sbom_dict.keys()
    assert "repo_name" in sbom_dict.keys()
    assert "repo_version" in sbom_dict.keys()
    assert "scored_dependencies" in sbom_dict.keys()
    assert "unscored_dependencies" in sbom_dict.keys()
    assert "failed_dependencies" in sbom_dict.keys()


def test_sbom_validation(sbom_bad):
    """
    Test that an exception is raised when an SBOM is invalid.
    """
    with pytest.raises(Exception):
        Sbom(sbom_bad)


def test_sbom_dependency_manager(sbom_from_json):
    """
    Test that the dependency manager is correctly initialized.
    """
    sbom = Sbom(sbom_from_json)
    assert sbom.dependency_manager is not None
    assert len(sbom.get_failed_dependencies()) == 0
    assert len(sbom.get_scored_dependencies()) == 0
    assert len(sbom.get_unscored_dependencies()) == 13


def test_sbom_dependency_manager_update(sbom_from_json):
    """
    Test that the dependency manager is correctly updated.
    """
    sbom = Sbom(sbom_from_json)
    assert sbom.dependency_manager is not None
    new_dep1 = Dependency(DUMMY_DEPENDENCIES[0])
    new_dep2 = Dependency(DUMMY_DEPENDENCIES[1])
    sbom.update_dependencies([new_dep1, new_dep2])
    assert len(sbom.get_failed_dependencies()) == 0
    assert len(sbom.get_scored_dependencies()) == 0
    assert len(sbom.get_unscored_dependencies()) == 15
