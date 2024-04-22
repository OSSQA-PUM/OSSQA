"""
This script defines a command-line argument parser for the Open Source Security
and Quality Assessment (OSSQA) program.

The script uses the argparse module to define and parse command-line arguments
for two commands: analyze and lookup.

The analyze command takes several arguments including the file path to the SBOM
JSON file, user requirements for the software, git token, output type,
and verbosity.

The lookup command takes the ID of the SBOM as an argument.
The script also includes helper functions to parse and validate the arguments.
"""

import os
import json
from argparse import ArgumentParser, Namespace
from argparse import RawTextHelpFormatter
from tabulate import tabulate
import requests
from data_types.user_requirements import UserRequirements, RequirementsType
from data_types.sbom_types.sbom import Sbom
from data_types.sbom_types.dependency import Dependency
from frontend.front_end_api import FrontEndAPI

parser = ArgumentParser(description=
"""Open Source Security and Quality Assessment

This program will help ensure security and high quality of software. 
By iterating a SBOM in CycloneDX format it will give you a result 
from the OpenSSF Scorecards scores of every involved component.""",
formatter_class=RawTextHelpFormatter)

run_type_group = parser.add_mutually_exclusive_group(required=True)

parser.usage = \
"""python3 arg_parser.py [-h --help] [-a --analyze] [-l --lookup] [flags]

Analyze flags:
    -p   --path                     (required)
    -r   --requirements
    -wc  --code-vulnerabilities
    -wm  --maintenance
    -wt  --continuous-testing
    -ws  --source-risk-assessment
    -wb  --build-risk-assessment
    -g   --git-token                (required)
    -o   --output
    -v   --verbose

Lookup flags:
    -i   --id                       (required)
    -o   --output                   
    -v   --verbose
    
"""

run_type_group.add_argument(
    "-a", "--analyze",
    action="store_true", help="Analyze SBOM file."
)
run_type_group.add_argument(
    "-l", "--lookup", action="store_true",
    help="Lookup SBOM in database."
)


# Analyze command
parser.add_argument(
    "-p", "--path", metavar='\b', type=str, 
    help="    The file path to the SBOM JSON file."
)

parser.add_argument(
    "-r", "--requirements", metavar='\b', type=str, 
    help=
"""The user requirements for the software. Input a list of weights, 
integers between 0-10. Like the following: [wc, wm, wt, ws, wb]"""
)

parser.add_argument(
    "-wc", "--code-vulnerabilities", metavar='\b', type=int,
    help = "Weight of vulnerability checks. Integer between 0-10."
)

parser.add_argument(
    "-wm", "--maintenance", metavar='\b', type=int,
    help = "Weight of maintenance checks. Integer between 0-10."
)

parser.add_argument(
    "-wt", "--continuous-testing", metavar='\b', type=int,
    help = "Weight of continuous testing checks. Integer between 0-10."
)

parser.add_argument(
    "-ws", "--source-risk-assessment", metavar='\b', type=int,
    help = "Weight of source risk assessment checks. Integer between 0-10."
)

parser.add_argument(
    "-wb", "--build-risk-assessment", metavar='\b', type=int,
    help = "Weight of build risk assessment checks. Integer between 0-10."
)

parser.add_argument(
    "-g", "--git-token", metavar='\b', type=str,
    help="    The git token."
)


# Lookup command
parser.add_argument(
    "-i", "--id", metavar='\b', type=int, 
    help="    The ID of the SBOM."
)

# Shared
parser.add_argument(
    "-o", "--output", metavar='\b', type=str,
    help="    Type of output to be returned. Choose 'simplified' or 'json'."
)

parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="Verbose output."
)

args: Namespace = parser.parse_args()

def parse_requirements(args:Namespace) -> UserRequirements:
    """
    Parse the requirements from the arguments.

    Args:
        args (Namespace): The arguments.

    Returns:
        UserRequirements: The user requirements.
    
    Raises:
        SystemExit: If the requirements are invalid.
    """
    requirements: list[int] = args.requirements.replace(" ", "") \
                                        .replace("[", "").replace("]", "") \
                                        .split(",")

    if args.code_vulnerabilities:
        requirements[0] = args.code_vulnerabilities
    if args.maintenance:
        requirements[1] = args.maintenance
    if args.continuous_testing:
        requirements[2] = args.continuous_testing
    if args.source_risk_assessment:
        requirements[3] = args.source_risk_assessment
    if args.build_risk_assessment:
        requirements[4] = args.build_risk_assessment

    try:
        assert len(requirements) == 5

        for i, req in enumerate(requirements):
            requirements[i] = int(req)
            assert 0 <= requirements[i] <= 10
    except (AssertionError, ValueError):
        print("requirements must be a list of 5 integers between 0 and 10.\n"+ \
              "Example: --requirements [10,10,3,4,5]")
        exit(1)

    requirements: UserRequirements = UserRequirements(
        {
            RequirementsType.CODE_VULNERABILITIES: requirements[0],
            RequirementsType.MAINTENANCE: requirements[1],
            RequirementsType.CONTINUOUS_TESTING: requirements[2],
            RequirementsType.SOURCE_RISK_ASSESSMENT: requirements[3],
            RequirementsType.BUILD_RISK_ASSESSMENT: requirements[4]
        }
    )

    return requirements


def check_token_usage(git_token: str = None):
    """
    Check the usage of the GitHub Personal Access Token.

    Returns:
        dict: A dictionary containing the token usage information, 
              including the limit, used, and remaining counts.
              Returns None if the authentication fails.
    """

    # Replace 'your_token_here' with your actual GitHub Personal Access Token
    if not git_token:
        token = os.environ.get('GITHUB_AUTH_TOKEN')
    else:
        token = git_token

    # The GitHub API URL for the authenticated user
    url = 'https://api.github.com/user'

    # Make a GET request to the GitHub API with your token for authentication
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers, timeout=5)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.headers

        return {
            "limit": user_data['X-RateLimit-Limit'],
            "used": user_data['x-ratelimit-used'],
            "remaining": user_data['X-RateLimit-Remaining']
        }

    raise ValueError("Failed to authenticate token. "
                     + f"Status code: {response.status_code}")


def parse_analyze_arguments(args: Namespace) -> None:
    """
    Parses and analyzes the command line arguments.

    Args:
        args (Namespace): The command line arguments.

    Returns:
        Tuple[str, UserRequirements]: 
            A tuple containing the path and user requirements.
    
    Raises:
        SystemExit: If the required argument [-p | --path] is missing.
    """
    if not args.path:
        print("Please add the argument [-p | --path] [PATH]")
        exit(1)

    path: str = args.path

    if not args.requirements:
        args.requirements = "10,10,10,10,10"

    requirements: UserRequirements = parse_requirements(args)

    git_token: str = args.git_token
    if not check_token_usage(git_token):
        print("Invalid git token, add argument [-g | --git-token] [YOUR TOKEN]")
        exit(1)

    if git_token:
        os.environ["GITHUB_AUTH_TOKEN"] = git_token

    return path, requirements


def parse_lookup_arguments(args: Namespace) -> int:
    """
    Parses the lookup arguments and returns the ID.

    Args:
        args (Namespace): The parsed command-line arguments.

    Returns:
        int: The ID extracted from the arguments.

    Raises:
        SystemExit: If the required argument [-i | --id] is missing.
    """
    if not args.id:
        print("Please add the argument [-i | --id] [ID]")
        exit(1)

    id: int = args.id
    return id


def parse_arguments_shared(args: Namespace) -> None:
    """
    Parses the shared arguments and returns the output and verbose values.

    Args:
        args (Namespace): The parsed command-line arguments.

    Returns:
        Tuple[str, bool]: A tuple containing the output value and verbose value.
    """
    output: str = "table"
    verbose: bool = False

    if args.output:
        output: str = args.output

    if args.verbose:
        verbose: bool = args.verbose

    return output, verbose


def calculate_mean_score(dependency: Dependency, decimals: int = 1) -> float:
    """
    Calculate the mean score of a dependency.

    Args:
        dependency (Dependency): The dependency to calculate the mean score for.
        decimals (int): The number of decimals to round the mean score to.
    
    Returns:
        float: The mean score of the dependency.
    """
    mean_score = 0
    for dep_score in dependency.dependency_score.checks:
        mean_score += dep_score.score
    mean_score /= len(dependency.dependency_score.checks)
    mean_score = round(mean_score, decimals)

    return mean_score


def get_mean_scores(dependencies:list[Dependency]) -> list[list[Dependency, float]]:
    """
    Calculate the mean scores of the dependencies.

    Args:
        dependencies (list[Dependency]): The dependencies to calculate the mean scores for.
    
    Returns:
        list[list[Dependency, float]]: A list of lists containing the dependency and the mean score.
    """
    mean_scores: list = []

    for dependency in dependencies:
        mean_score = calculate_mean_score(dependency)    
        dep_result = [dependency.name, mean_score]
        mean_scores.append(dep_result)
    return mean_scores


def main():
    """
    Main function that handles the execution of the program.
    """
    output, verbose = parse_arguments_shared(args)

    if args.analyze:
        path, requirements = parse_analyze_arguments(args)
        with open(path) as f:
            sbom_dict:dict = json.load(f)
            sbom = Sbom(sbom_dict)

        print(sbom.to_dict())
        api = FrontEndAPI()
        # TODO handle errors
        scored_sbom: Sbom = api.analyze_sbom(sbom, requirements)

        scores = scored_sbom.dependency_manager.get_scored_dependencies()

        if args.output != "json":
            print(tabulate(get_mean_scores(scores), headers=["Dependency", "Average Score"]))
        else:
            json_results = scored_sbom.dependency_manager.to_dict()
            print(json_results)
        return

    id = parse_lookup_arguments(args)
    print(id)
    print(output, verbose)


if __name__ == "__main__":
    main()

# Proposed calculation
# 10-(10-S)*(P/10)
