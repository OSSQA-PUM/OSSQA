import json
import requests
from multiprocessing import Pool
import tqdm

def parse_git_url(url: str) -> tuple[str, str, str]:
    url_split = url.replace("https://", "").split("/")
    platform = url_split[0]

    if platform != "github.com":
        raise ValueError("Platform not supported")

    repo_owner = url_split[1]
    repo_name = url_split[2]

    return platform, repo_owner, repo_name


def get_component_url(component: dict) -> str:
    external_refs = component.get("externalReferences")
    if not external_refs:
        raise KeyError("No external references found")
    
    for external_ref in external_refs:
        if external_ref["type"] != "vcs":
            continue

        url = external_ref["url"]
        try:
            response = requests.get(url, timeout=5)
        except requests.ConnectTimeout:
            raise ConnectionError(f"Connection to {url} timed out")

        if response.status_code != 200:
            raise ConnectionError(f"Failed to connect to {url}")

        response_url = response.url
        
        return response_url
    
    raise NameError("No VCS external reference found")

def load_sbom_data(sbom_file: str) -> dict:
    with open(sbom_file, "r") as file:
        sbom_data = json.load(file)
    
    return sbom_data

def parse_component(component: dict) -> tuple[str, str, str, str]:
    try:
        respose_url = get_component_url(component=component)
        platform, repo_owner, repo_name = parse_git_url(respose_url)
        return platform, repo_owner, repo_name, respose_url
    except Exception as e:
        print(e, component["name"])

if __name__ == "__main__":
    """url = "https://git-wip-us.apache.org/repos/asf?p=commons-lang.git"
    component = {
        "externalReferences": [
            {
                "type": "vcs",
                "url": url
            }
        ]
    }"""

    sbom_dict = load_sbom_data("C:/Programming/Kandidat/OSSQA/src/bom.json")
    components = sbom_dict["components"]

    success = 0

    with Pool() as pool, tqdm.tqdm(total=len(components)) as pbar:
        for dependencie_data in pool.imap_unordered(parse_component, components):
            #print(dependencie_data)
            if dependencie_data:
                #print(dependencie_data)
                success += 1
            pbar.update(1)

    print(f"Success: {success}/{len(components)}")

    """for component in components:
        
        try:
            respose_url = get_component_url(component=component)
            print(parse_git_url(respose_url))
        except (KeyError, NameError, ValueError, ConnectionError) as e:
            print(e)"""