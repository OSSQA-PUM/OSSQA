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
from argparse import ArgumentParser, Namespace
from argparse import RawTextHelpFormatter
from tabulate import tabulate
import requests
import json

from util import UserRequirements, check_token_usage

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
    help="    Type of output to be returned. Example 'json'."
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
        requirements[0], requirements[1], requirements[2],
        requirements[3], requirements[4]
    )

    return requirements


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


def main():
    """
    Main function that handles the execution of the program.
    """
    output, verbose = parse_arguments_shared(args)

    if args.analyze:
        path, requirements = parse_analyze_arguments(args)
        with open(path) as f:
            sbom:str = f.read()
        dict_weighted_results: list[(str, int, str)] #(checkname, score, dependency)
        dict_weighted_results = requests.post(
            json=sbom, headers={"user_reqs": str(requirements)}, 
            url="http://host.docker.internal:98" + "/analyze"
        ).text

        print(dict_weighted_results)
        #dict_weighted_results = result.json()
        #print(tabulate(dict_weighted_results,
        #                headers=["Checkname", "Score", "Dependency"]))
        return

    id = parse_lookup_arguments(args)
    print(id)
    print(output, verbose)


if __name__ == "__main__":
    main()
