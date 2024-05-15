"""
Represents a dependency manager that manages dependencies for a project.
"""
from typing import Callable
from main.data_types.sbom_types.dependency import Dependency


class DependencyManager:
    """
    Represents a dependency manager that manages dependencies for a project.
    """
    _dependencies: list[Dependency]

    def __init__(self, sbom_components: list[dict]):
        """
        Initialize the dependency manager.

        Args:
            sbom_components (list[dict]): The components of the SBOM.
        """
        self._dependencies = \
            [Dependency(component) for component in sbom_components]

    def update(self, dependencies: list[Dependency]):
        """
        Update existing dependencies or add new ones if they do not exist.
        Dependencies are unique and identified by their platform, repo_path,
        and version.

        Args:
            dependencies (list[Dependency]): The dependencies to update.
        """
        for dependency in dependencies:
            try:
                index = self._dependencies.index(dependency)
                if dependency.scorecard or dependency.failure_reason:
                    # We only want scored or failed dependencies
                    self._dependencies[index] = dependency
            except ValueError:
                self._dependencies.append(dependency)

    def get_scored_dependencies(self) -> list[Dependency]:
        """
        Get the scored dependencies.

        Returns:
            list[Dependency]: The scored dependencies.
        """
        return list(
            filter(
                    lambda dependency: dependency.scorecard
                    and not dependency.failure_reason,
                    self._dependencies
                )
            )

    def get_unscored_dependencies(self) -> list[Dependency]:
        """
        Get the unscored dependencies.

        Returns:
            list[Dependency]: The unscored dependencies.
        """
        return list(
            filter(
                    lambda dependency: not dependency.scorecard
                    and not dependency.failure_reason,
                    self._dependencies
                )
            )

    def get_failed_dependencies(self) -> list[Dependency]:
        """
        Get the failed dependencies.

        Returns:
            list[Dependency]: The failed dependencies.
        """
        return list(
            filter(
                    lambda dependency: dependency.failure_reason,
                    self._dependencies
                )
            )

    def get_dependencies_by_filter(self, dependency_filter: Callable) \
            -> list[Dependency]:
        """
        Get the dependencies by filter.

        Args:
            dependency_filter (Callable): The filter to apply.

        Returns:
            list[Dependency]: The dependencies that satisfy the filter.
        """
        return list(filter(dependency_filter, self._dependencies))

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary containing
                scored_dependencies: list[dict],
                unscored_dependencies: list[dict],
                failed_dependencies: list[dict].
        """
        return {
            'scored_dependencies':
                [dependency.to_dict() for dependency
                    in self.get_scored_dependencies()],
            'unscored_dependencies':
                [dependency.to_dict() for dependency
                    in self.get_unscored_dependencies()],
            'failed_dependencies':
                [dependency.to_dict() for dependency
                    in self.get_failed_dependencies()]
        }
    
    def to_dict_web(self) -> dict:
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary containing
                scored_dependencies: list[dict],
                unscored_dependencies: list[dict],
                failed_dependencies: list[dict].
        """
        return {
            'scored_dependencies':
                [dependency.to_dict_web() for dependency
                    in self.get_scored_dependencies()],
            'unscored_dependencies':
                [dependency.to_dict_web() for dependency
                    in self.get_unscored_dependencies()],
            'failed_dependencies':
                [dependency.to_dict_web() for dependency
                    in self.get_failed_dependencies()]
        }
