import requests
from util import Dependency


def add_SBOM(sbom_json: dict, dependencies: list[Dependency]):
    """
    Adds a SBOM to the database
    Args:
        sbom_json: dict 
        An SBOM as a json object.
        dependencies: list[Dependency]
        The dependencies of the SBOM.

    Returns:
        int:
        Status code of the request
    """
    data = {}
    try:
        data["serialNumber"] = sbom_json["serialNumber"]
    except KeyError:
        data["serialNumber"] = sbom_json["$schema"]
    data['version'] = sbom_json["version"]
    data["name"] = sbom_json["metadata"]["name"]
    data["repo_version"] = sbom_json["metadata"]["version"]

    data["components"] = [{
        "name": dep.json_component["name"],
        "version": dep.json_component["version"],
        "score": dep.dependency_score["score"],
        "checks": dep.dependency_score["checks"],
    } for dep in dependencies]

    r = requests.post("localhost:5080/add_SBOM", json=data)
    return r.status_code


# ossqa history
def get_history():
    """
    Gets previus SBOMs
    Returns:
        list:
        A list of the previous SBOMs

    """
    response = requests.get("localhost:5080/get_history")
    return response.json()


# ossqa history [ID]
def get_SBOM(id: int):
    """
    Gets a specific SBOM
    Args:
        id:
        int: The id of the SBOM
    Returns:

    """
    response = requests.get("localhost:5080/get_SBOM", data={"id": id})
    return response.json()


def get_existing_dependencies(needed_dependencies: list):
    """
    Gets the existing dependencies
    Args:
        needed_dependencies:
        A list of the needed dependencies
    Returns:
        list:
        A list of the existing dependencies as Dependency objects
    """
    dependency_primary_keys = []
    for i in range(len(needed_dependencies)):
        json_obj = needed_dependencies[i].json_component
        dependency_primary_keys.append({'name': json_obj['name'], 'version': json_obj['version']})

    all_depencency_objects = requests.get("localhost:5080/get_existing_dependencies",
                                          data=dependency_primary_keys).json()
    result = []
    for i in range(len(all_depencency_objects)):
        current = all_depencency_objects[i]
        url_split = current['name'].replace("https://", "").split("/")
        dep_obj = Dependency(
            dependency_score={'score': current['score'], 'checks': current['checks']},
            platform=url_split[0],
            repo_owner=url_split[1],
            repo_name=url_split[2],
            url=current['name']
        )
        result.append(dep_obj)
    return result
