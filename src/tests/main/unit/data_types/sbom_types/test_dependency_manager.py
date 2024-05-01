"""
This module contains unit tests for the `DependencyManager` class in the
`dependency_manager` module of the `sbom_types` package.

The `DependencyManager` class is responsible for managing dependencies in a
software bill of materials (SBOM). It provides methods for initializing the
manager, updating the dependencies, and converting the manager to a
dictionary representation.

The unit tests in this module cover the initialization of the
`DependencyManager` class, the conversion of the manager to a dictionary,
and the updating of dependencies. The tests also cover the retrieval of scored,
unscored, and failed dependencies from the manager.
"""

import json
import pytest
from main.data_types.sbom_types.dependency_manager import DependencyManager
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.scorecard import Scorecard
from tests.main.unit.scorecards.scorecards import PATHS
from tests.main.unit.data_types.sbom_types.expected_jsons.expected_results \
    import PATHS as expected_paths


@pytest.fixture
def dependency_manager_5_dependencies():
    """
    Fixture to create a DependencyManager with 5 dependencies.
    """
    dep1 = Dependency(
        name="dep1", git_url="github.com/repo/path", version="1.0"
        )
    dep2 = Dependency(
        name="dep2", git_url="github.com/repo/path", version="2.0"
        )
    dep3 = Dependency(
        name="dep3", git_url="github.com/repo/path", version="3.0"
        )
    dep4 = Dependency(
        name="dep4", git_url="github.com/repo/path", version="4.0"
        )
    dep5 = Dependency(
        name="dep5", git_url="github.com/repo/path", version="5.0"
        )
    dependencies = [dep1, dep2, dep3, dep4, dep5]
    dependency_manager = DependencyManager()
    dependency_manager.update(dependencies)
    return dependency_manager


@pytest.fixture
def dependency_manager_with_score():
    """
    Fixture to create a DependencyManager with a scored dependency.
    """
    dep1 = Dependency(name="d1", git_url="github.com/repo/path", version="1.0")
    with (open(PATHS[0], "r", encoding="utf-8")) as file:
        scorecard = Scorecard(json.load(file))
    dep1.dependency_score = scorecard
    dependency_manager = DependencyManager()
    dependency_manager.update([dep1])
    return dependency_manager


@pytest.fixture
def dependency_manager_failed_dependency():
    """
    Fixture to create a DependencyManager with a failed dependency.
    """
    dep1 = Dependency(name="d1", git_url="github.com/repo/path", version="1.0")
    dep1.failure_reason = Exception("Failed to fetch dependency")
    dependency_manager = DependencyManager()
    dependency_manager.update([dep1])
    return dependency_manager


@pytest.fixture
def dep_mangr_with_distict_deps():
    """
    Fixture to create a DependencyManager with scored, unscored, and failed
    dependencies."""
    dep1 = Dependency(
        name="dep1", git_url="github.com/repo/path", version="1.0"
        )
    with (open(PATHS[1], "r", encoding="utf-8")) as file:
        scorecard = Scorecard(json.load(file))
    dep1.dependency_score = scorecard
    dep2 = Dependency(
        name="dep2", git_url="github.com/repo/path", version="1.0"
        )
    dep2.failure_reason = Exception("Failed to fetch dependency")
    dependency_manager = DependencyManager()
    dep3 = Dependency(
        name="dep3", git_url="github.com/repo/path", version="1.0"
        )
    dependency_manager.update([dep1, dep2, dep3])
    return dependency_manager


def test_dependency_manager_initialization():
    """
    Test the initialization of the DependencyManager class.
    """
    assert DependencyManager()


def test_dependency_empty_manager_to_dict():
    """
    Test the to_dict method of the DependencyManager class when the manager is
    empty."""
    dependency_manager = DependencyManager()
    assert dependency_manager.to_dict() == {"scored_dependencies": [],
                                            "unscored_dependencies": [],
                                            "failed_dependencies": []}


def test_dependency_manager_update():
    """
    Test the update method of the DependencyManager class when the manager is
    updated with a new dependency."""
    dependency_manager = DependencyManager()
    dep1 = Dependency(
        name="dep1", git_url="github.com/repo/path", version="1.0"
        )
    dependency_manager.update([dep1])
    assert len(dependency_manager.get_unscored_dependencies()) == 1


def test_dependency_manager_get_scored_dependencies(
        dependency_manager_with_score):
    """
    Test the get_scored_dependencies method of the DependencyManager class when
    the manager has scored dependencies."""
    assert len(dependency_manager_with_score.get_scored_dependencies()) == 1


def test_dependency_manager_get_unscored_dependencies(
        dependency_manager_5_dependencies):
    """
    Test the get_unscored_dependencies method of the DependencyManager class 
    when the manager has unscored dependencies."""
    dependency_manager = dependency_manager_5_dependencies
    assert len(dependency_manager.get_unscored_dependencies()) == 5


def test_dependency_manager_get_failed_dependencies(
        dependency_manager_failed_dependency):
    """
    Test the get_failed_dependencies method of the DependencyManager class when
    the manager has a failed dependency."""
    dependency_manager = dependency_manager_failed_dependency
    assert len(dependency_manager.get_failed_dependencies()) == 1


def test_dependency_manager_get_unscored_scored_and_failed_dependencies(
        dep_mangr_with_distict_deps):
    """
    Test the get_unscored_dependencies, get_scored_dependencies, and
    get_failed_dependencies methods of the DependencyManager class when the
    manager has scored, unscored, and failed dependencies."""
    dependency_manager = dep_mangr_with_distict_deps
    assert len(dependency_manager.get_unscored_dependencies()) == 1
    assert len(dependency_manager.get_scored_dependencies()) == 1
    assert len(dependency_manager.get_failed_dependencies()) == 1


def test_dependency_manager_update_same_dependency(
        dependency_manager_5_dependencies):
    """
    Test the update method of the DependencyManager class when the same
    dependency is updated multiple times."""
    dependency_manager = dependency_manager_5_dependencies
    new_dep = Dependency(
        name="dep5", git_url="github.com/repo/path", version="5.0"
        )
    dependency_manager.update([new_dep])
    dependency_manager.update([new_dep])
    dependency_manager.update([new_dep])
    dependency_manager.update([new_dep])
    dependency_manager.update([new_dep])
    assert len(dependency_manager.get_unscored_dependencies()) == 5


def test_dependency_manager_replace_scored_with_unscored(
        dependency_manager_with_score):
    """
    Test the update method of the DependencyManager class when a scored
    dependency is replaced with an unscored dependency.
    """
    dependency_manager = dependency_manager_with_score
    new_dep = Dependency(
        name="d1", git_url="github.com/repo/path", version="1.0"
        )
    dependency_manager.update([new_dep])
    assert len(dependency_manager.get_unscored_dependencies()) == 0
    assert len(dependency_manager.get_scored_dependencies()) == 1


def test_dependency_manager_to_dict_filled(
        dep_mangr_with_distict_deps
):
    """
    Test the to_dict method of the DependencyManager class when the manager
    has scored, unscored, and failed dependencies.
    """
    dependency_manager = dep_mangr_with_distict_deps
    with (open(expected_paths[0], "r", encoding="utf-8")) as file:
        expected = json.load(file)
    dep_dict = dependency_manager.to_dict()
    print(dep_dict)
    assert dep_dict["scored_dependencies"][0]["dependency_score"] == expected
    assert dep_dict["unscored_dependencies"] == \
        [{'name': 'dep3',
          'git_url': 'github.com/repo/path',
          'version': '1.0',
          'dependency_score': None,
          'failure_reason': None}]
    assert isinstance(
        dep_dict["failed_dependencies"][0]["failure_reason"], str
        )


def test_dependency_manager_get_by_filter(dep_mangr_with_distict_deps):
    """
    Test the get_dependencies_by_filter method of the DependencyManager class.
    """
    dependency_manager = dep_mangr_with_distict_deps

    scored_deps = dependency_manager.get_dependencies_by_filter(
        lambda dep: dep.dependency_score
    )
    unscored_deps = dependency_manager.get_dependencies_by_filter(
        lambda dep: not dep.dependency_score
    )
    failed_deps = dependency_manager.get_dependencies_by_filter(
        lambda dep: dep.failure_reason
    )
    all_deps = dependency_manager.get_dependencies_by_filter(
        lambda dep: True
    )

    assert len(scored_deps) == 1
    assert len(unscored_deps) == 2
    assert len(failed_deps) == 1
    assert len(all_deps) == 3
