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
import json
import os
from pathlib import Path

import click
import requests
import validators
from tabulate import tabulate

import main.constants as constants
from main.data_types.sbom_types.dependency import Dependency
from main.data_types.sbom_types.sbom import Sbom
from main.data_types.user_requirements import (RequirementsType,
                                               UserRequirements)
from main.frontend.front_end_api import FrontEndAPI
from main.util import raise_github_token_refused


def calculate_mean_score(dependency: Dependency, decimals: int = 1) -> float:
    """
    Calculate the mean score of a dependency.

    Args:
        dependency (Dependency): The dependency to calculate the
        mean score for.

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


def calculate_mean_scores(dependencies: list[Dependency]) -> \
                                                list[list[Dependency, float]]:
    """
    Calculate the mean scores of the dependencies.

    Args:
        dependencies (list[Dependency]): The dependencies to calculate the
        mean scores for.

    Returns:
        list[list[Dependency, float]]: A list of lists containing the
        dependency and the mean score.
    """
    mean_scores: list = []

    for dependency in dependencies:
        mean_score = calculate_mean_score(dependency)
        dep_result = [dependency.component_name, mean_score, dependency.reach_requirement]
        mean_scores.append(dep_result)
    return mean_scores


def color_score(name: str, score: float, requirement: str) -> \
                                                        list[str, str, str]:
    """
    Color the score based on the value.

    Args:
        name (str): The name of the dependency.
        score (float): The score of the dependency.

    Returns:
        list[str, str]: A list containing the dependency name and
        the colored score.
    """
    if requirement == "No" or requirement == "Test result not found":
        return [f"\033[91m{name}\033[0m", f"\033[91m{score}\033[0m",
                f"\033[91m{requirement}\033[0m"]

    if score >= 7:
        return [f"\033[92m{name}\033[0m", f"\033[92m{score}\033[0m",
                f"\033[92m{requirement}\033[0m"]

    if score >= 3:
        return [f"\033[93m{name}\033[0m", f"\033[93m{score}\033[0m",
                f"\033[93m{requirement}\033[0m"]

    return [f"\033[91m{name}\033[0m", f"\033[91m{score}\033[0m",
            f"\033[91m{requirement}\033[0m"]


def color_scores(scores: list[list[Dependency, float, str]]) -> \
                                                        list[list[str, str, str]]:
    """
    Color the scores based on the values.

    Args:
        scores (list[list[Dependency, float]]): The dependency scores.

    Returns:
        list[list[str, str]]: A list of lists containing the
        colored dependency name and score.
    """
    colored_scores: list = []

    for score in scores:
        colored_score = color_score(score[0], score[1], score[2])
        colored_scores.append(colored_score)
    return colored_scores


def parse_requirements(**kwargs) -> UserRequirements:
    """
    Parses the requirements from the arguments.

    Args:
        **kwargs (Any): The arguments.

    Returns:
        UserRequirements: The parsed user requirements.
    """
    vulnerabilities: int = kwargs.get("vulnerabilities")
    dependency_update_tool: int = kwargs.get("dependency_update_tool")
    maintained: int = kwargs.get("maintained")
    security_policy: int = kwargs.get("security_policy")
    license: int = kwargs.get("license")
    cii_best_practices: int = kwargs.get("cii_best_practices")
    ci_tests: int = kwargs.get("ci_tests")
    fuzzing: int = kwargs.get("fuzzing")
    sast: int = kwargs.get("sast")
    binary_artifacts: int = kwargs.get("binary_artifacts")
    branch_protection: int = kwargs.get("branch_protection")
    dangerous_workflow: int = kwargs.get("dangerous_workflow")
    code_review: int = kwargs.get("code_review")
    contributors: int = kwargs.get("contributors")
    pinned_dependencies: int = kwargs.get("pinned_dependencies")
    token_permissions: int = kwargs.get("token_permissions")
    packaging: int = kwargs.get("packaging")
    signed_releases: int = kwargs.get("signed_releases")

    return UserRequirements({
        RequirementsType.VULNERABILITIES: vulnerabilities,
        RequirementsType.DEPENDENCY_UPDATE_TOOL: dependency_update_tool,
        RequirementsType.MAINTAINED: maintained,
        RequirementsType.SECURITY_POLICY: security_policy,
        RequirementsType.LICENSE: license,
        RequirementsType.CII_BEST_PRACTICES: cii_best_practices,
        RequirementsType.CI_TESTS: ci_tests,
        RequirementsType.FUZZING: fuzzing,
        RequirementsType.SAST: sast,
        RequirementsType.BINARY_ARTIFACTS: binary_artifacts,
        RequirementsType.BRANCH_PROTECTION: branch_protection,
        RequirementsType.DANGEROUS_WORKFLOW: dangerous_workflow,
        RequirementsType.CODE_REVIEW: code_review,
        RequirementsType.CONTRIBUTORS: contributors,
        RequirementsType.PINNED_DEPENDENCIES: pinned_dependencies,
        RequirementsType.TOKEN_PERMISSIONS: token_permissions,
        RequirementsType.PACKAGING: packaging,
        RequirementsType.SIGNED_RELEASES: signed_releases
    })

def table_output(scored_sbom: Sbom):
    """
    Print the output in a table format.
    Args:
        scored_sbom (Sbom): The scored SBOM.
    """
    scored_deps = scored_sbom.dependency_manager.get_scored_dependencies()
    failed_deps = scored_sbom.dependency_manager.get_failed_dependencies()
    mean_scores = calculate_mean_scores(scored_deps)
    mean_scores = sorted(mean_scores, key=lambda x: x[1])
    mean_scores = color_scores(mean_scores)
    failed_deps = [
        [dep.component_name, dep.failure_reason] for dep in failed_deps
    ]
    print(
        tabulate(
            mean_scores, 
            headers=[
                "Successful Dependencies", 
                "Average Score", 
                "Meet requirements?"
            ]
        )
    )
    print(
        tabulate(
            failed_deps, 
            headers=["Failed Dependencies", "Failure Reason"]
        )
    )


def json_output(scored_sbom: Sbom):
    """
    Print the output in a JSON format.
    Args:
        scored_sbom (Sbom): The scored SBOM.
    """
    deps_dict = scored_sbom.dependency_manager.to_dict()
    print(json.dumps(deps_dict))


def simplified_output(scored_sbom: Sbom):
    """
    Print the output in a simplified format.
    
    Args:
        scored_sbom (Sbom): The scored SBOM.
    """
    scored_deps = scored_sbom.dependency_manager.get_scored_dependencies()
    failed_deps = scored_sbom.dependency_manager.get_failed_dependencies()
    mean_scores = calculate_mean_scores(scored_deps)
    mean_scores = sorted(mean_scores, key=lambda x: x[1])
    failed_deps = [[dep.component_name, dep.failure_reason] 
                   for dep in failed_deps]

    print("Successfull dependencies:")
    for dep in mean_scores:
        print(f"{dep[0]},{dep[1]},{dep[2]}")

    print("\nFailed dependencies:")
    for dep in failed_deps:
        print(f"{dep[0]},{dep[1]}")

def validate_backend(_ctx, _param, value: str):
    """
    Validates that the backend URL is a valid URL.
    """
    value = value.replace("localhost", "127.0.0.1")
    validation_res = validators.url(value)
    if isinstance(validation_res, validators.ValidationError):
        print(validation_res)
        raise click.BadParameter("Invalid backend URL.")
    else:
        return value


def validate_git_token(_ctx, _param, value: str):
    """
    Validates that a GitHub Personal Access Token is valid.
    """
    if not value:
        raise click.BadParameter("Please set environment variable "
                                 "'GITHUB_AUTH_TOKEN' or provide a "
                                 "non-empty string.")

    url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {value}"}
    response = requests.get(url, headers=headers, timeout=5)

    match response.status_code:
        case 401:
            raise click.BadParameter("Your GitHub token could not be "
                                     "authenticated (HTTP 401).")
        case _:
            return value


@click.group(context_settings={"max_content_width": 120, "show_default": True})
def ossqa_cli():
    """
    The entry point of the program.
    """


@ossqa_cli.command(help="Analyze the given SBOM.")
@click.argument("path", required=True,
                type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("-g", "--git-token", type=str, envvar="GITHUB_AUTH_TOKEN",
              callback=validate_git_token,
              help=("GitHub Personal Access Token."
                    "  [default: GITHUB_AUTH_TOKEN env variable]"))
@click.option("-v", "--vulnerabilities", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for vulnerabilities.")
@click.option("-dut", "--dependency-update-tool", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for dependency update tool.")
@click.option("-m", "--maintained", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for maintained.")
@click.option("-sp", "--security-policy", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Reuirement for security policy.")
@click.option("-l", "--license", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Reuirement for license.")
@click.option("-cbp", "--cii-best-practices", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for CII best practices.")
@click.option("-ct", "--ci-tests", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for CI tests.")
@click.option("-f", "--fuzzing", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for fuzzing.")
@click.option("-s", "--sast", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for SAST.")
@click.option("-ba", "--binary-artifacts", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for binary artifacts.")
@click.option("-bp", "--branch-protection", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for branch protection.")
@click.option("-dw", "--dangerous-workflow", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for dangerous workflow.")
@click.option("-cr", "--code-review", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for code review.")
@click.option("-c", "--contributors", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for contributors.")
@click.option("-pd", "--pinned-dependencies", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for pinned dependencies.")
@click.option("-tp", "--token-permissions", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for contributors.")
@click.option("-p", "--packaging", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for packaging.")
@click.option("-sr", "--signed-releases", type=click.IntRange(-1, 10),
              required=False, default=-1,
              help="Requirement for signed releases.")

@click.option("-b", "--backend", type=str, callback=validate_backend,
              default=constants.HOST, help="URL of the database server.")
@click.option("-o", "--output", type=click.Choice(["table",
                                                   "simplified",
                                                   "json"]),
              required=False, default="table",
              help="Output format.")
@click.option("-v", "--verbose", is_flag=True, default=False, required=False,
              help="Verbose output.")
def analyze(path: Path, git_token: str, backend: str, output: str, **kwargs):
    """
    Executes the command that analyzes an SBOM.
    """
    requirements = parse_requirements(**kwargs)
    with open(path, "r", encoding="utf-8") as file:
        unscored_sbom = Sbom(json.load(file))

    # TODO: git_token should be sent to the frontend API, instead of setting
    #       os.environ, to be more traceable
    os.environ["GITHUB_AUTH_TOKEN"] = git_token

    front_end_api = FrontEndAPI(backend)
    scored_sbom = front_end_api.analyze_sbom(unscored_sbom, requirements)

    match output:
        case "table":
            table_output(scored_sbom)
        case "json":
            json_output(scored_sbom)
        case "simplified":
            simplified_output(scored_sbom)
        case _:
            print("Unrecognized output format.")


@ossqa_cli.command(help="Lookup names of SBOMs in the database.")
@click.option("-b", "--backend", type=str, callback=validate_backend,
              default=constants.HOST, help="URL of the database server.")
@click.option("-o", "--output", type=click.Choice(["table", "json"]),
              required=False, default="table",
              help="Output format.")
@click.option("-v", "--verbose", is_flag=True, default=False, required=False,
              help="Verbose output.")
def sboms(backend: str, output: str, verbose: str):
    """
    Executes the command that fetches all SBOM names from the backend.
    """
    front_end_api = FrontEndAPI(backend)
    sbom_names = front_end_api.lookup_stored_sboms()

    if output == "table":
        table = tabulate([sbom_names], headers=["Repository Names"])
        print(table)
    elif output == "json":
        print(json.dumps(sbom_names))
    else:
        print("This code should be unreachable.")


@ossqa_cli.command(help="Lookup SBOMs with a given name.")
@click.argument("name", required=True, type=str)
@click.option("-b", "--backend", type=str, callback=validate_backend,
              default=constants.HOST, help="URL of the database server.")
@click.option("-o", "--output", type=click.Choice(["table", "json"]),
              required=False, default="table",
              help="Output format.")
@click.option("-v", "--verbose", is_flag=True, default=False, required=False,
              help="Verbose output.")
def lookup(name: str, backend: str, output: str, verbose: str):
    """
    Executes the command that fetches all SBOMs of a specific name
    from the backend.
    """
    front_end_api = FrontEndAPI(backend)
    found_sboms = front_end_api.lookup_previous_sboms(name)

    if output == "table":
        table_data = []
        for sbom in found_sboms:
            dependencies = sbom.dependency_manager.get_dependencies_by_filter(
                lambda _: True
            )
            sbom_data = [
                sbom.serial_number,
                sbom.version,
                sbom.repo_name,
                sbom.repo_version,
                len(dependencies),
            ]
            table_data.append(sbom_data)

        table_headers = [
            "Serial number",
            "Version",
            "Repo name",
            "Repo version",
            "Dependency count"
        ]
        table = tabulate(table_data, headers=table_headers)
        print(table)
    elif output == "json":
        sbom_dicts = [sbom.to_dict() for sbom in found_sboms]
        print(json.dumps(sbom_dicts))
