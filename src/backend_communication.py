"""
This module provides functions for communicating with the backend
and managing SBOMs (Software Bill of Materials).
"""

import requests

from util import Dependency

host = "http://localhost:5080"


def add_sbom(sbom_json: dict, dependencies: list[Dependency]):
    print("\n")
    """
    Adds a SBOM to the database.

    Args:
        sbom_json (dict): An SBOM as a json object.
        dependencies (list[Dependency]): The dependencies of the SBOM.

    Returns:
        int: Status code of the request.
    """
    data = {}
    try:
        data["serialNumber"] = sbom_json["serialNumber"]
    except KeyError:
        data["serialNumber"] = sbom_json["$schema"]
    data['version'] = sbom_json["version"]
    tools = sbom_json["metadata"]["tools"]
    data["name"] = tools[0]["name"]
    data["repo_version"] = tools[0]["version"]

    data["components"] = [{
        "name": dep.json_component["name"],
        "version": dep.json_component["version"],
        "score": dep.dependency_score["score"],
        "checks": dep.dependency_score["checks"],
    } for dep in dependencies]

    r = requests.post(host + "/add_SBOM", json=data, timeout=5)
    return r.status_code


# ossqa history
def get_history():
    """
    Gets previous SBOMs.

    Returns:
        list: The previous SBOMs.
    """
    response = requests.get(host + "/get_history", timeout=5)
    return response.json()


# ossqa history [ID]
def get_sbom(sbom_id: int):
    """
    Gets a specific SBOM.

    Args:
        sbom_id (int): The ID of the SBOM.

    Returns:
        dict: A dictionary-representation of the SBOM.
    """
    response = requests.get(
        host + "/get_SBOM",
        data={"id": sbom_id},
        timeout=5)
    return response.json()


def get_existing_dependencies(needed_dependencies: list[Dependency]):
    """
    Gets the existing dependencies.

    Args:
        needed_dependencies (list[Dependency]): The needed dependencies.

    Returns:
        list: A list of the existing dependencies.
    """
    dependency_primary_keys = []
    for i in range(len(needed_dependencies)):
        json_obj = needed_dependencies[i].json_component
        dependency_primary_keys.append((json_obj['name'], json_obj['version']))

    all_dependencies = requests.get(
        host + "/get_existing_dependencies",
        data=dependency_primary_keys,
        timeout=5
    )
    print("all dependencies:" + str(all_dependencies.request))
    print("all dependencies json:" + str(all_dependencies.json()))
    result = []
    all_dependencies = all_dependencies.json()
    # TODO: research why .json() removes "name_version" from the object
    for dependency in all_dependencies:
        print("!!!!!!!dependency!!!!!!! " + str(dependency))
        # url_split = dependency['name'].replace("https://", "").split("/")
        url_split = dependency['name_version'].split("/").split("@")
        dep_obj = Dependency(dependency_score={'score': dependency['score'], 'checks': dependency['checks']},
                             platform=url_split[0],
                             repo_owner=url_split[1],
                             repo_name=url_split[2],
                             url=dependency['name']
                             )
        result.append(dep_obj)
    return result
