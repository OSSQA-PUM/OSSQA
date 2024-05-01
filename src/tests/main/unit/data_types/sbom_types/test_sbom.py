"""
This module contains unit tests for the `Sbom` class in the
`sbom` module of the `sbom_types` package.
"""
import json
import re
import pytest
from tests.main.unit.sboms.sboms import (PATHS as SBOM_PATHS,
                                         BAD_SBOMS,
                                         SBOM_COMPONENT_URLS,
                                         DUMMY_SBOM)
from main.data_types.sbom_types.sbom import Sbom


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
    assert len(sbom.dependency_manager.get_failed_dependencies()) == 0
    assert len(sbom.dependency_manager.get_scored_dependencies()) == 0
    assert len(sbom.dependency_manager.get_unscored_dependencies()) == 13


def test_parse_git_url(sbom_component_url):
    """
    Test that the `_parse_git_url` method returns the correct URL.
    """
    sbom = Sbom(DUMMY_SBOM)

    if sbom_component_url.startswith("https://"):
        parsed_url = sbom._parse_github_url(sbom_component_url)
        assert sbom_component_url.lstrip("https:/") == parsed_url
    else:
        with pytest.raises(Exception):
            sbom._parse_github_url(sbom_component_url)


def test_get_component_url(sbom_component):
    """
    Test that the `_get_component_url` method returns the correct URL.
    """
    sbom = Sbom(DUMMY_SBOM)
    component_url = sbom._parse_component_name(sbom_component)
    print(component_url)
    assert component_url is not None
    assert re.match(
        r"github.com\/[^\/]+\/[^\/]+", component_url
        ) is not None


def test_get_component_url_bad():
    """
    Test that the `_get_component_url` method raises an exception when the
    component is invalid.
    """
    sbom = Sbom(DUMMY_SBOM)
    with pytest.raises(Exception):
        sbom._parse_component_name({"bad": "component"})
