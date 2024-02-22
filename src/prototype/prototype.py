from multiprocessing import Pool
from typing import List, Tuple
import subprocess
import json

import tqdm

def analyze_dependency_score(git_url: str) -> List[Tuple[str, int, str]]:
    """
    Analyzes the dependencies of a given Git repository using the OpenSSF Scorecard tool.
    
    Args:
        git_url (str): The URL of the Git repository to analyze.
        git_auth_token (str, optional): Authentication token for accessing private repositories. 
            Defaults to reading from a file if not provided.
    
    Returns:
        A list of tuples containing the name, score, and URL of each dependency check.
    """
    # Load the Git authentication token from a file if not provided
    #if git_auth_token == "":
    #    git_auth_token = open('git_token.txt', 'r').readline()
    
    # Execute the Scorecard tool in a Docker container, passing the necessary environment variables
    output = subprocess.check_output(
        f'scorecard --repo={git_url} --show-details --format json', 
        shell=True
    )
    
    # Decode and clean the output for JSON parsing
    output = output.decode("utf-8")
    output = output.replace("failed to get console mode for stdout: The handle is invalid.", "")
    output = output.replace("\n", "")

    #print(output)

    json_output = json.loads(output) 

    dependency_scores = []
    
    # Extract and store the score for each check performed by the Scorecard tool
    for check in json_output["checks"]:
        dependency_scores.append((check['name'], check['score'], git_url))
    
    return dependency_scores

def analyze_multiple_dependency_scores(git_urls: List[str]) -> List[List[Tuple[str, int, str]]]:
    """
    Analyzes the dependencies of multiple Git repositories concurrently using the OpenSSF Scorecard.
    
    Args:
        git_urls (List[str]): URLs of the Git repositories to analyze.
        git_auth_token (str, optional): Authentication token for accessing private repositories. 
            Defaults to reading from a file if not provided.
    
    Returns:
        A list of lists, where each inner list contains the dependency scores for a Git repository.
    """
    dependency_scores = []
    analyze_amount = len(git_urls)
    analyzed = 0

    with Pool() as pool, tqdm.tqdm(total=analyze_amount) as pbar:
        for scores in pool.imap_unordered(analyze_dependency_score, git_urls):
            dependency_scores.append(scores)
            analyzed += 1
            pbar.update(1)
    
    
    return dependency_scores

def get_dependency_urls(SBOM) -> List[str]:
    """
    Extracts URLs of dependencies from a Software Bill of Materials (SBOM) file.
    
    Args:
        SBOM: The SBOM file in JSON format.
    
    Returns:
        A list of URLs of the dependencies.
    """
    data = json.load(SBOM)
    component_urls = []
    
    # Filter and collect URLs that start with 'github'
    for component in data["components"]:
        url = component["name"]
        if url.startswith("github"):
            component_urls.append(url)

    print(f"URLs extracted: {len(component_urls)} out of {len(data['components'])}")
    return component_urls

def calculate_sbom_scores(dependency_scores: List[List[Tuple[str, int, str]]]) -> List[Tuple[str, int, str]]:
    """
    Calculates the scores for each dependency category based on their dependency scores.
    
    Args:
        dependency_scores (List[List[Tuple[str, int, str]]]): Dependency scores for multiple repositories.
    
    Returns:
        A list of tuples with the category name, lowest score, and the URL of the dependency.
    """
    if not dependency_scores:
        return []
    
    # Initialize scores with high values to easily find the minimum
    scores = [("", 100000)] * len(dependency_scores[0])

    # Update scores with the lowest found for each category
    for dependency in dependency_scores:
        for i in range(len(dependency)):
            if dependency[i][1] < scores[i][1]:
                scores[i] = dependency[i]

    return scores

def prototype():
    """
    Executes the prototype analysis, aggregating dependency scores from multiple repositories.
    """
    # Open and process the SBOM file
    SBOM = open('example-SBOM.json')
    component_urls = get_dependency_urls(SBOM)
    dependency_scores = analyze_multiple_dependency_scores(component_urls)
    summary = calculate_sbom_scores(dependency_scores)

    # Print a summary of the analysis
    for summary_item in summary:
        print(f"{summary_item[0]}, Score: {summary_item[1]}, cause: {summary_item[2]}")

if __name__ == "__main__":
    prototype()