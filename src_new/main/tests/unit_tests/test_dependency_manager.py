import pytest
from data_types.sbom_types.dependency_manager import DependencyManager
from data_types.sbom_types.dependency import Dependency

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
    assert len(dependency_manager._dependencies) == 1
    
def test_dependency_manager_update_same_dependency(
        dependency_manager_5_dependencies):
    new_dep = Dependency(name="github.com/repo/path", version="5.0")
    dependency_manager_5_dependencies.update([new_dep])
    assert len(dependency_manager_5_dependencies._dependencies) == 5
    
