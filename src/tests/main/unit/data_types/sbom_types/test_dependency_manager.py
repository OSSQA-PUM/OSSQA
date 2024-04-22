"""
This module contains unit tests for the `DependencyManager` class in the
`dependency_manager` module of the `sbom_types` package.

The `DependencyManager` class is responsible for managing dependencies in a
software bill of materials (SBOM). It provides methods for initializing the
manager, updating the dependencies, and converting the manager to a
dictionary representation.

The unit tests in this module cover the initialization of the
`DependencyManager` class, the conversion of the manager to a dictionary,
and the updating of dependencies.

"""

import json
import pytest
from main.data_types.sbom_types.dependency_manager import DependencyManager
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from tests.main.unit.scorecards.scorecards import PATHS
from tests.main.unit.data_types.sbom_types.expected_jsons.expected_results import PATHS as expected_paths


@pytest.fixture
def dependency_manager_5_dependencies():
    dep1 = Dependency(name="github.com/repo/path", version="1.0")
    dep2 = Dependency(name="github.com/repo/path", version="2.0")
    dep3 = Dependency(name="github.com/repo/path", version="3.0")
    dep4 = Dependency(name="github.com/repo/path", version="4.0")
    dep5 = Dependency(name="github.com/repo/path", version="5.0")
    dependencies = [dep1, dep2, dep3, dep4, dep5]
    dependency_manager = DependencyManager()
    dependency_manager.update(dependencies)
    return dependency_manager


@pytest.fixture
def dependency_manager_with_score():
    dep1 = Dependency(name="github.com/repo/path", version="1.0")
    with (open(PATHS[0], "r")) as file:
        scorecard = Scorecard(json.load(file))
    dep1.dependency_score = scorecard
    dependency_manager = DependencyManager()
    dependency_manager.update([dep1])
    return dependency_manager


@pytest.fixture
def dependency_manager_failed_dependency():
    dep1 = Dependency(name="github.com/repo/path", version="1.0")
    dep1.failure_reason = Exception("Failed to fetch dependency")
    dependency_manager = DependencyManager()
    dependency_manager.update([dep1])
    return dependency_manager


@pytest.fixture
def dependency_manager_with_unscore_score_and_failed_dependency():
    dep1 = Dependency(name="github.com/repo/path", version="1.0")
    with (open(PATHS[1], "r")) as file:
        scorecard = Scorecard(json.load(file))
    dep1.dependency_score = scorecard
    dep2 = Dependency(name="github.com/repo/path", version="2.0")
    dep2.failure_reason = Exception("Failed to fetch dependency")
    dependency_manager = DependencyManager()
    dep3 = Dependency(name="github.com/repo/path", version="3.0")
    dependency_manager.update([dep1, dep2, dep3])
    return dependency_manager


def test_dependency_manager_initialization():
    assert DependencyManager()


def test_dependency_manager_to_dict():
    dependency_manager = DependencyManager()
    assert dependency_manager.to_dict() == {"scored_dependencies": [],
                                            "unscored_dependencies": [],
                                            "failed_dependencies": []}


def test_dependency_manager_update():
    dependency_manager = DependencyManager()
    dep1 = Dependency(name="github.com/repo/path", version="1.0")
    dependency_manager.update([dep1])
    assert len(dependency_manager.get_unscored_dependencies()) == 1


def test_dependency_manager_get_scored_dependencies(
        dependency_manager_with_score):
    assert len(dependency_manager_with_score.get_scored_dependencies()) == 1


def test_dependency_manager_get_unscored_dependencies(
        dependency_manager_5_dependencies):
    dependency_manager = dependency_manager_5_dependencies
    assert len(dependency_manager.get_unscored_dependencies()) == 5


def test_dependency_manager_get_failed_dependencies(
        dependency_manager_failed_dependency):
    dependency_manager = dependency_manager_failed_dependency
    assert len(dependency_manager.get_failed_dependencies()) == 1


def test_dependency_manager_get_unscored_scored_and_failed_dependencies(
        dependency_manager_with_unscore_score_and_failed_dependency):
    dependency_manager = dependency_manager_with_unscore_score_and_failed_dependency
    assert len(dependency_manager.get_unscored_dependencies()) == 1
    assert len(dependency_manager.get_scored_dependencies()) == 1
    assert len(dependency_manager.get_failed_dependencies()) == 1


def test_dependency_manager_update_same_dependency(
        dependency_manager_5_dependencies):
    dependency_manager = dependency_manager_5_dependencies
    new_dep = Dependency(name="github.com/repo/path", version="5.0")
    dependency_manager.update([new_dep])
    assert len(dependency_manager.get_unscored_dependencies()) == 5


def test_dependency_manager_replace_scored_with_unscored(
        dependency_manager_with_score):
    dependency_manager = dependency_manager_with_score
    new_dep = Dependency(name="github.com/repo/path", version="1.0")
    dependency_manager.update([new_dep])
    assert len(dependency_manager.get_unscored_dependencies()) == 0
    assert len(dependency_manager.get_scored_dependencies()) == 1


def test_dependency_manager_to_dict_filled(
        dependency_manager_with_unscore_score_and_failed_dependency
):
    dependency_manager = dependency_manager_with_unscore_score_and_failed_dependency
    with (open(expected_paths[0], "r")) as file:
        expected = json.load(file)
    assert dependency_manager.to_dict()["scored_dependencies"][0]["dependency_score"] == expected
    assert dependency_manager.to_dict()["unscored_dependencies"] == [{'name': 'github.com/repo/path', 'version': '3.0', 'dependency_score': '', 'failure_reason': ''}]
    assert isinstance(dependency_manager.to_dict()["failed_dependencies"][0]["failure_reason"], Exception)
