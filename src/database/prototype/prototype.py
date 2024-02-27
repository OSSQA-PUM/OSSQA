# def calculate_sbom_scores(dependency_scores: List[List[Tuple[str, int, str]]]) -> List[Tuple[str, int, str]]:
#     if not dependency_scores:
#         return []
    
#     # Initialize scores with high values to easily find the minimum
#     scores = [("", 100000)] * len(dependency_scores[0])

#     # Update scores with the lowest found for each category
#     for dependency in dependency_scores:
#         for i in range(len(dependency)):
#             if dependency[i][1] < scores[i][1]:
#                 scores[i] = dependency[i]

#     return scores

# def prototype():
#     """
#     Executes the prototype analysis, aggregating dependency scores from multiple repositories.
#     """
#     # Open and process the SBOM file
#     SBOM = open('example-SBOM.json')
#     component_urls = get_dependency_urls(SBOM)
#     dependency_scores = analyze_multiple_dependency_scores(component_urls)
#     summary = calculate_sbom_scores(dependency_scores)

#     # Print a summary of the analysis
#     for summary_item in summary:
#         print(f"{summary_item[0]}, Score: {summary_item[1]}, cause: {summary_item[2]}")

from multiprocessing import Pool
import json
import subprocess
import tqdm


def get_dependency_urls(sbom_data: dict) -> list[str]:
    dependency_urls = []

    for component in sbom_data["components"]:
        if external_refs := component.get("externalReferences"):
            for external_ref in external_refs:
                if external_ref["type"] == "vcs":
                    url = external_ref["url"]
                    github_idx = url.find("github.com")
                    #gitlab_idx = url.find("gitlab.com")

                    if github_idx != -1:
                        url = url[github_idx:]

                    # NOTE: we cant run scorecard on gitlab if we dont have
                    #       a gitlab auth token
                    #elif gitlab_idx != -1:
                    #    url = url[gitlab_idx:]
                    
                    if url.endswith(".git"):
                        url = url[:-4]

                    dependency_urls.append(url)
                    break

    print(f"URLs extracted: {len(dependency_urls)} out of {len(sbom_data['components'])}")
    return dependency_urls


def analyze_dependency(dependency_url: str) -> tuple[list[tuple[str, int, str]], dict]:
    output = ""
    try:
        output = subprocess.check_output(
            f'scorecard --repo={dependency_url} --show-details --format json', 
            shell=True,
        )
    except subprocess.CalledProcessError:
        # Failed scorecard means the repo is unreachable (probably doesn't exist)
        return None, None

    output = output.decode("utf-8")
    output = output.replace("failed to get console mode for stdout: The handle is invalid.", "")
    output = output.replace("\n", "")

    json_output = json.loads(output)

    scores = []
    for check in json_output["checks"]:
        scores.append((check['name'], check['score'], dependency_url))

    return scores, json_output


def analyze_dependencies(dependency_urls: list[str]) -> tuple[list[str], list[dict]]:
    dependency_scores = []
    scorecard_outputs = []

    analyze_amount = len(dependency_urls)
    analyzed = 0

    with Pool() as pool, tqdm.tqdm(total=analyze_amount) as pbar:
        for scores, output in pool.imap_unordered(analyze_dependency, dependency_urls):
            if scores is not None and output is not None:
                dependency_scores.append(scores)
                scorecard_outputs.append(output)
                analyzed += 1
            pbar.update(1)

    return dependency_scores, scorecard_outputs


def main():
    sbom_path = "SBOM2.json"
    results_path = sbom_path.replace(".json", "_results.json")
    
    with open(sbom_path, "r") as file:
        sbom_data = json.load(file)

    dependency_urls = get_dependency_urls(sbom_data)
    dependency_scores, scorecard_outputs = analyze_dependencies(dependency_urls)

    sbom_data["components"] = scorecard_outputs
    with open(results_path, "w") as file:
        json.dump(sbom_data, file, indent=3)


if __name__ == "__main__":
    main()