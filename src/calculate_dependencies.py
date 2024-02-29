

from multiprocessing import Pool
from dataclasses import dataclass
import json
import requests
import tqdm

@dataclass
class Dependency:
    """
    Represents a dependency for a project.

    Attributes:
        json_component (dict): The JSON representation of the dependency.
        platform (str): The platform on which the dependency is used.
        repo_owner (str): The owner of the repository 
                          where the dependency is hosted.
        repo_name (str): The name of the repository 
                         where the dependency is hosted.
        url (str): The URL of the dependency.
        failure_reason (Exception): The reason for any failure 
                                    related to the dependency.
        dependency_score (dict): The scorecard related to the dependency.
    """
    json_component: dict
    platform: str = None
    repo_owner: str = None
    repo_name: str = None
    url: str = None
    failure_reason: Exception = None
    dependency_score: dict = None


def parse_git_url(url: str) -> tuple[str, str, str]:
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
    url_split = url.replace("https://", "").split("/")
    platform = url_split[0]

    if platform != "github.com":
        raise ValueError("Platform not supported")

    repo_owner = url_split[1]
    repo_name = url_split[2]

    return platform, repo_owner, repo_name


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
        dependency.platform, \
        dependency.repo_owner, \
        dependency.repo_name = parse_git_url(dependency.url)
    except (ConnectionError, KeyError, NameError, ValueError) as e:
        dependency.failure_reason = e
    return dependency


def parse_sbom(sbom: dict) \
    -> tuple[list[Dependency], list[Dependency], dict]:
    """
    Parses the SBOM (Software Bill of Materials) 
    and returns the dependencies, failures, and failure reasons.

    Args:
        sbom_file (dict): The path to the SBOM JSON file.

    Returns:
        tuple[list[Dependency], list[Dependency], dict]: The dependencies, 
        failures, and failure reasons.
    """
    print("Parsing SBOM")
    components = sbom["components"]

    dependencies_data:list[Dependency] = []
    failures: list[Dependency] = []
    failure_reason: dict = {}
    success = 0

    with Pool() as pool, tqdm.tqdm(total=len(components)) as progress_bar:
        for dependency in pool.imap_unordered(parse_component, components):
            if dependency.failure_reason:
                exception_type = type(dependency.failure_reason)
                failures.append(dependency.json_component)
                failure_reason[exception_type] = failure_reason.get(
                    exception_type, 0) + 1
                progress_bar.update(1)
                continue

            dependencies_data.append(dependency)
            success += 1
            progress_bar.update(1)
    print(f"Successfully parsed {success}/{len(components)} components.")

    return dependencies_data, failures, failure_reason


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
                            {dependency.repo_owner}/{dependency.repo_name}
                            /commits""", timeout=10)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()[0]["sha"]
    else:
        return None


def try_get_from_ssf_api(dependency: Dependency, commit_sha1 = None):
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
    + f"{dependency.platform}/{dependency.repo_owner}/{dependency.repo_name}"
    + (f"?commit={commit_sha1}" if commit_sha1 else ""), timeout=10)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return None


def lookup_database(needed_dependencies : list[Dependency]) \
    -> tuple[list[Dependency], list[Dependency]]:
    """
    Looks up the needed dependencies in the database 
    and returns the dependencies with scores and the new needed dependencies.

    Args:
        needed_dependencies (list[Dependency]): 
        The list of needed dependencies.

    Returns:
        tuple[list[Dependency], list[Dependency]]: 
        The dependencies with scores and the new needed dependencies.
    """
    dependencies_with_scores = []

    # TODO try to get needed_dependencies scores from our database
    # Assume database response is in the same order as needed_dependencies
    # fake database response for now
    # (the database did not have any of the needed dependencies)
    database_response = [None] * len(needed_dependencies)

    # Calculate the dependencies that are not in the database
    print("Looking up dependencies in database")
    success = 0
    new_needed_dependencies = []
    with tqdm.tqdm(total=len(needed_dependencies)) as progress_bar:
        for database_response, dependency in zip(
            database_response, needed_dependencies):
            if database_response is None:
                new_needed_dependencies.append(dependency)
            else:
                dependency.dependency_score = database_response
                dependencies_with_scores.append(dependency)
                success += 1
            progress_bar.update(1)
    print(f"Successfully looked up {success}/{len(needed_dependencies)} "
          + "dependencies in the database.")
    return dependencies_with_scores, new_needed_dependencies


def lookup_ssf(dependency: Dependency) -> dict:
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


def lookup_multiple_ssf(needed_dependencies : list[Dependency]) \
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
    print("Looking up dependencies in the SSF API")
    new_needed_dependencies = []
    work_count = len(needed_dependencies)
    success = 0
    with Pool() as pool, tqdm.tqdm(total=work_count) as progress_bar:
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
    print("Successfully looked up " \
          + f"{success}/{work_count} dependencies in the SSF API.")

    return dependencies_with_scores, new_needed_dependencies


def get_dependencies(sbom: dict) \
    -> tuple[list[Dependency], list[Dependency], list[Dependency]]:
    """
    Retrieves the dependencies from the SBOM (Software Bill of Materials) 
    and performs database and SSF (Security Scorecards) lookups.

    Args:
        sbom_file (str): The path to the SBOM JSON file.

    Returns:
        tuple[list[Dependency], list[Dependency]]: The dependency scores, 
        new needed dependencies, and failures.
    """
    dependencies, failures, failure_reason = parse_sbom(sbom=sbom)
    needed_dependencies = dependencies
    total_dependency_count = len(dependencies)

    #print(failure_reason)

    # TODO try to recover failed components
    scores = []

    new_scores, needed_dependencies = lookup_database(
        needed_dependencies=needed_dependencies)
    scores += new_scores

    new_scores, needed_dependencies = lookup_multiple_ssf(
        needed_dependencies=needed_dependencies)
    scores += new_scores

    print(
        "Could not find stored data for "
        + f"{len(needed_dependencies)}/{total_dependency_count} dependencies.")

    return scores, needed_dependencies, failures


if __name__ == "__main__":
    SBOM_PATH = "E:/programming/OSSQA/src/bom.json"
    with open(SBOM_PATH, "r", encoding="utf-8") as file:
        sbom_data = json.load(file)
    scores, needed, failures = get_dependencies(sbom=sbom_data)
    print(needed[0])
