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
from main.data_types.user_requirements import RequirementsType, UserRequirements
from main.frontend.front_end_api import FrontEndAPI


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


def calculate_mean_scores(dependencies:list[Dependency]) -> \
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
        dep_result = [dependency.name, mean_score]
        mean_scores.append(dep_result)
    return mean_scores


def color_score(name: str, score: float) -> list[str, str]:
    """
    Color the score based on the value.

    Args:
        name (str): The name of the dependency.
        score (float): The score of the dependency.

    Returns:
        list[str, str]: A list containing the dependency name and
        the colored score.
    """
    if score >= 7:
        return [f"\033[92m{name}\033[0m", f"\033[92m{score}\033[0m"]
    elif score >= 3:
        return [f"\033[93m{name}\033[0m", f"\033[93m{score}\033[0m"]
    else:
        return [f"\033[91m{name}\033[0m", f"\033[91m{score}\033[0m"]


def color_scores(scores: list[list[Dependency, float]]) -> \
                                                        list[list[str, str]]:
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
        colored_score = color_score(score[0], score[1])
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
    code_vulnerabilities: int = kwargs.get("code_vulnerabilities")
    maintenance: int = kwargs.get("maintenance")
    continuous_testing: int = kwargs.get("continuous_testing")
    source_risk_assessment: int = kwargs.get("source_risk_assessment")
    build_risk_assessment: int = kwargs.get("build_risk_assessment")

    return UserRequirements({
        RequirementsType.CODE_VULNERABILITIES: code_vulnerabilities,
        RequirementsType.MAINTENANCE: maintenance,
        RequirementsType.CONTINUOUS_TESTING: continuous_testing,
        RequirementsType.SOURCE_RISK_ASSESSMENT: source_risk_assessment,
        RequirementsType.BUILD_RISK_ASSESSMENT: build_risk_assessment,
    })


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
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {value}"}
    response = requests.get(url, headers=headers, timeout=5)

    # TODO: Could do more extensive error-checking here.
    #       For example, different messages for different status codes.
    if response.status_code != 200:
        raise click.BadParameter("Failed to authenticate token. "
                                 + f"Status code: {response.status_code}")
    else:
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

@click.option("-wc", "--code-vulnerabilities", type=click.IntRange(0, 10),
              required=False, default=10,
              help="Weight for Code Vulnerabilities category.")
@click.option("-wm", "--maintenance", type=click.IntRange(0, 10),
              required=False, default=10,
              help="Weight for Maintenance category.")
@click.option("-wt", "--continuous-testing", type=click.IntRange(0, 10),
              required=False, default=10,
              help="Weight for Continuous Testing category.")
@click.option("-ws", "--source-risk-assessment", type=click.IntRange(0, 10),
              required=False, default=10,
              help="Weight for Source Risk Assessment category.")
@click.option("-wb", "--build-risk-assessment", type=click.IntRange(0, 10),
              required=False, default=10,
              help="Weight for Build Risk Assesment category.")

@click.option("-b", "--backend", type=str, callback=validate_backend,
              default=constants.HOST, help="URL of the database server.")
@click.option("-o", "--output", type=click.Choice(["table", "json"]),
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

    if output == "table":
        scored_deps = scored_sbom.dependency_manager.get_scored_dependencies()
        failed_deps = scored_sbom.dependency_manager.get_failed_dependencies()

        mean_scores = calculate_mean_scores(scored_deps)
        mean_scores = sorted(mean_scores, key=lambda x: x[1])
        mean_scores = color_scores(mean_scores)

        failed_deps = [[dep.name, dep.failure_reason] for dep in failed_deps]

        print(
            tabulate(mean_scores, headers=["Successful Dependencies", "Average Score"])
        )
        print(
            tabulate(failed_deps, headers=["Failed Dependencies", "Failure Reason"])
        )
    elif output == "json":
        deps_dict = scored_sbom.dependency_manager.to_dict()
        print(json.dumps(deps_dict))
    else:
        print("This code should be unreachable.")


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
    else:
        print("This code should be unreachable.")
