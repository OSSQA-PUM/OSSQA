"""
This file contains functions for parsing and analyzing dependencies
in a Software Bill of Materials (SBOM).
It includes functions for parsing the SBOM,
retrieving dependency information from external sources,
and looking up dependency scores
from a database and the Security Scorecards API.
"""

import json
import subprocess
from multiprocessing import Pool
from typing import Any
from urllib.parse import urlparse
import requests

import tqdm

from util import Dependency, validate_scorecard
from job_observer import JobModelSingleton, JobStatus

job_model = JobModelSingleton()


def parse_git_url(url: str) -> tuple[str, str]:
    """
    Parses the git URL and returns the platform,
    repository owner, and repository name.

    Args:
        url (str): The git URL.

    Returns:
        tuple[str, str, str]: The platform, repository owner,
        and repository name.

    Raises:
        ValueError: If the platform is not supported.
    """
    url_split = urlparse(url)
    platform = url_split.netloc

    if platform != "github.com":
        raise ValueError("Platform not supported")

    repo_path = url_split.path

    return platform, repo_path


def get_component_url(component: dict) -> str:
    """
    Retrieves the URL of a component from its external references.

    Args:
        component (dict): The component dictionary.

    Returns:
        str: The URL of the component.

    Raises:
        KeyError:
        If no external references are found.

        ConnectionError:
        If there is a connection error while accessing the URL.

        NameError:
        If no VCS (Version Control System) external reference is found.
    """
    external_refs = component.get("externalReferences")
    if not external_refs:
        raise KeyError("No external references found")
    for external_ref in external_refs:
        if external_ref["type"] != "vcs":
            continue

        url = external_ref["url"]
        try:
            response = requests.get(url, timeout=5)
        except (requests.ConnectTimeout, requests.ReadTimeout) as e:
            raise ConnectionError(f"Connection to {url} timed out") from e
        except requests.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to {url}") from e

        if response.status_code != 200:
            raise ConnectionError(f"Failed to connect to {url}")

        response_url = response.url
        return response_url
    raise NameError("No VCS external reference found")


def parse_component(component: dict) -> Dependency:
    """
    Parses a component dictionary and returns a Dependency object.

    Args:
        component (dict): The component dictionary.

    Returns:
        Dependency: The parsed Dependency object.
    """
    dependency: Dependency = Dependency(json_component=component)
    try:
        dependency.url = get_component_url(component=component)
        dependency.platform, dependency.repo_path = parse_git_url(
                                                        dependency.url
                                                        )
        dependency.version = component["version"]
    except (ConnectionError, KeyError, NameError, ValueError) as e:
        dependency.failure_reason = e
    return dependency


def parse_sbom(sbom: dict) -> tuple[list[Dependency], list[Dependency], dict]:
    """
    Parses the SBOM (Software Bill of Materials)
    and returns the dependencies, failures, and failure reasons.

    Args:
        sbom (dict): The path to the SBOM JSON file.

    Returns:
        tuple[list[Dependency], list[Dependency], dict]: The dependencies,
        failures, and failure reasons.
    """
    components = sbom["components"]
    job_model.set_attributes(
        status=JobStatus.PARSING,
        message="Parsing SBOM...",
        max_dependency_count=len(components),
        success_dependency_count=0,
        subjob_max_dependency_count=len(components),
        subjob_success_dependency_count=0
    )

    dependencies_data: list[Dependency] = []
    failed_components: list[Dependency] = []
    failure_reason: dict = {}
    success = 0

    with Pool() as pool, tqdm.tqdm(total=len(components)) as progress_bar:
        for dependency in pool.imap(parse_component, components):
            if dependency.failure_reason:
                exception_type = type(dependency.failure_reason)
                failed_components.append(dependency.json_component)
                failure_reason[exception_type] = failure_reason.get(
                    exception_type, 0) + 1
                progress_bar.update(1)
                continue

            dependencies_data.append(dependency)
            success += 1
            progress_bar.update(1)
            job_model.subjob_success_dependency_count = success

    job_model.message = (
        f"Successfully parsed {job_model.subjob_success_dependency_count}/"
        f"{job_model.max_dependency_count} components."
    )

    return dependencies_data, failed_components, failure_reason


def get_git_sha1_number(dependency: Dependency) -> str:
    """
    Retrieves the SHA1 number of a dependency from the GitHub API.

    Args:
        dependency (Dependency): The dependency object.

    Returns:
        str: The SHA1 number of the dependency.
    """
    # Call the GitHub API
    response = requests.get(f"""https://api.github.com/repos/
                            {dependency.repo_path}/commits""",
                            timeout=10)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()[0]["sha"]
    return ""


def try_get_from_ssf_api(dependency: Dependency, commit_sha1=None)\
        -> dict[str, str] | None:
    """
    Retrieves the scorecard of a dependency
    from the SSF (Security Scorecards) API.

    Args:
        dependency (Dependency): The dependency object.
        commit_sha1 (str, optional): The SHA1 number of the commit.
                                     Defaults to None.

    Returns:
        dict: The scorecard of the dependency.
    """
    # Call the SSF API
    response = requests.get(
        "https://api.securityscorecards.dev/projects/"
        + f"{dependency.platform}/{dependency.repo_path}"
        + (f"?commit={commit_sha1}" if commit_sha1 else ""), timeout=10)

    # Check if the response is successful
    if response.status_code != 200:
        return None
    try:
        json_response = response.json()
    except (json.JSONDecodeError, KeyError):
        return None

    if not validate_scorecard(json_response):
        return None

    return json_response


def filter_database_dependencies(
        needed_dependencies: list[Dependency],
        database_dependencies: list[Dependency])\
            -> tuple[list[Dependency], list[Dependency]]:
    """
    Looks up the needed dependencies in the database
    and returns the dependencies with scores and the new needed dependencies.

    Args:
        database_dependencies:
        needed_dependencies (list[Dependency]):
        The list of needed dependencies.

    Returns:
        tuple[list[Dependency], list[Dependency]]:
        The dependencies with scores and the new needed dependencies.
    """
    dependencies_with_scores = []
    job_model.set_attributes(
        status=JobStatus.DATABASE_FILTER,
        message="Filtering database dependencies...",
        subjob_max_dependency_count=len(needed_dependencies),
        subjob_success_dependency_count=0
    )

    # Calculate the dependencies that are not in the database

    new_needed_dependencies = needed_dependencies.copy()
    success = 0

    with tqdm.tqdm(total=len(database_dependencies)) as progress_bar:
        for response in database_dependencies:
            if response in new_needed_dependencies:
                idx = new_needed_dependencies.index(response)
                dep = new_needed_dependencies.pop(idx)
                dep.dependency_score = response.dependency_score
                dependencies_with_scores.append(dep)
                job_model.increment_success()

            success += 1
            progress_bar.update(1)

    job_model.message = (
        f"Successfully looked up {job_model.subjob_success_dependency_count}/"
        f"{job_model.max_dependency_count} "
        "dependencies in the database."
    )

    # // TODO: Fix issue where new_needed_dependencies include all dependencies
    return dependencies_with_scores, new_needed_dependencies


def lookup_ssf(dependency: Dependency) -> dict[str, str] | None:
    """
    Looks up the scorecard of a dependency
    in the SSF (Security Scorecards) API.

    Args:
        dependency (Dependency): The dependency object.

    Returns:
        dict: The scorecard of the dependency.
    """
    sha1 = get_git_sha1_number(dependency)
    scorecard_score = try_get_from_ssf_api(dependency, sha1)
    return scorecard_score


def lookup_multiple_ssf(needed_dependencies: list[Dependency])\
        -> tuple[list[Dependency], list[Dependency]]:
    """
    Looks up the needed dependencies in the SSF (Security Scorecards) API
    and returns the dependencies with scores and the new needed dependencies.

    Args:
        needed_dependencies (list[Dependency]):
        The list of needed dependencies.

    Returns:
        tuple[list[Dependency], list[Dependency]]: The dependencies
        with scores and the new needed dependencies.
    """
    dependencies_with_scores = []
    new_needed_dependencies = []
    job_model.set_attributes(
        status=JobStatus.SSF_LOOKUP,
        message="Looking up dependencies in the SSF API...",
        subjob_max_dependency_count=len(needed_dependencies),
        subjob_success_dependency_count=0
    )
    success = 0
    with Pool() as pool, \
            tqdm.tqdm(total=len(needed_dependencies)) as progress_bar:
        for scorecard_score, dependency in zip(
                pool.imap_unordered(lookup_ssf, needed_dependencies),
                needed_dependencies):
            if scorecard_score is None:
                new_needed_dependencies.append(dependency)
                progress_bar.update(1)
                continue

            dependency.dependency_score = scorecard_score
            dependencies_with_scores.append(dependency)
            success += 1
            progress_bar.update(1)
            job_model.increment_success()

    job_model.message = (
        "Successfully looked up "
        f"{job_model.subjob_success_dependency_count}/"
        f"{job_model.max_dependency_count} dependencies in the SSF API.")

    return dependencies_with_scores, new_needed_dependencies


def analyse_score(dependency: Dependency):
    """
    Analyzes the score of a dependency.

    Args:
        dependency (Dependency): The dependency object.

    Returns:
        json_output: The scorecard of the dependency.
    """
    # Execute the Scorecard tool in a Docker container
    # passing the necessary environment variables
    url = dependency.url.replace("https://", "")

    output = subprocess.check_output(
        f'scorecard --repo={url} --show-details --format json',
        shell=True,
        stderr=subprocess.DEVNULL
    )

    # Decode and clean the output for JSON parsing
    output = output.decode("utf-8")
    output = output.replace(
        "failed to get console mode for stdout: The handle is invalid.", ""
    )
    output = output.replace("\n", "")

    json_output = json.loads(output)

    return json_output


def analyse_multiple_scores(dependencies: list[Dependency])\
        -> tuple[list[Dependency], list[Dependency]]:
    """
    Analyzes multiple scores for a list of dependencies.

    Args:
        dependencies (list[Dependency]):
        The list of dependencies to be analyzed.

    Returns:
        list[Dependency]: The list of dependencies with updated scores.
    """
    dependency_scores = []
    needed_dependencies = []
    job_model.set_attributes(
        status=JobStatus.ANALYZING_SCORE,
        message="Analyzing dependency scores...",
        subjob_max_dependency_count=len(dependencies),
        subjob_success_dependency_count=0
    )
    success = 0
    with Pool() as pool, tqdm.tqdm(total=len(dependencies)) as progress_bar:
        # A json serialized object is returned from analyze_score()
        dependency_score: Any
        for dependency, dependency_score in zip(
                dependencies, pool.imap_unordered(
                                                analyse_score, dependencies
                                                )):
            if dependency_score is None:
                needed_dependencies.append(dependency)
                progress_bar.update(1)
                continue
            dependency.dependency_score = dependency_score
            dependency_scores.append(dependency)
            progress_bar.update(1)
            success += 1
            job_model.increment_success()

    job_model.message = (
        "Successfully analyzed "
        f"{job_model.success_dependency_count}/"
        f"{job_model.max_dependency_count} dependencies")

    return dependency_scores, needed_dependencies
