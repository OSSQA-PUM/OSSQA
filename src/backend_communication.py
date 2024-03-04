import requests
from util import Dependency


def add_SBOM(json_file: dict):
    data = {}
    try:
        data["serialNumber"] = json_file["serialNumber"]
    except KeyError:
        data["serialNumber"] = json_file["$schema"]
    data["components"] = json_file["components"]
    data["name"] = json_file["metadata"]["name"]
    data["version"] = json_file["metadata"]["version"]
    r = requests.post("localhost:5080/add_SBOM", json=data)
    return r.status_code

# ossqa history
def get_history():
    response = requests.get("localhost:5080/get_history")
    return response.json()

# ossqa history [ID]
def get_SBOM(id: int):
    response = requests.get("localhost:5080/get_SBOM", data={"id": id})
    return response.json()


def get_existing_dependencies(needed_dependencies: list):
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
            repo_name = url_split[2],
            url=current['name']
        )
        result.append(dep_obj)
    return result