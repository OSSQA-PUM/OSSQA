# OSSQA

## Description

This is the official repository for the Open Source Security and Quality Assessment (OSSQA) project. 
OSSQA is a project for determining the quality of a software projekt using a Software Bill of Materials (SBOM).

## Getting Started

### Installing

To install OSSQA, clone this repository
```
git clone https://github.com/OSSQA-PUM/OSSQA.git
```

### Executing program

1. Build the Docker image
```
docker compose build ossqa-cli
```

2. Run a container of the image
```
docker compose run ossqa-cli [COMMAND] [ARGUMENTS…]
```


## Analyze Command
This command analyzes an SBOM and scores its components. The components are scored with OpenSSF Scorecard which runs many tests of five different categories. Scorecard requires a GitHub Personal Access Token which can be created according to [these instructions](https://github.com/ossf/scorecard?tab=readme-ov-file#authentication)

* Usage:
  ```
  docker compose run ossqa-cli analyze PATH [OPTIONS…]
  ```
* Example:
  ```
  docker compose run ossqa-cli analyze /sboms/example-SBOM.json -sp 6
  ```

### Prepositionals
| Prepositional      | Description |
| ----------- | ----------- |
| PATH      | Path to the SBOM file.       |

### Options
| Option      | Description |
| ----------- | ----------- |
| -g \| --git-token      | A GitHub Personal Access Token. Defaults to the GITHUB_AUTH_TOKEN environment variable in the docker image.       |
| -v \| --vulnerabilities   | Requirement for vulnerabilities from -1 to 10.        |
| -dut \| –dependency-update-tool   | Requirement for dependency update tool from -1 to 10.        |
| -m \| --maintained   | Requirement for maintained from -1 to 10.        |
| -sp \| --security-policy   | Requirement for security policy from -1 to 10.        |
| -l \| --license   | Requirement for license from -1 to 10.        |
| -cbp \| --cii-best-practices   | Requirement for CII best practices from -1 to 10.        |
| -ct \| --ci-tests   | Requirement for CI tests from -1 to 10.        |
| -f \| --fuzzing   | Requirement for fuzzing from -1 to 10.        |
| -s \| --sast   | Requirement for SAST from -1 to 10.        |
| -ba \| --binary-artifacts   | Requirement for binary artifacts from -1 to 10.        |
| -bp \| --branch-protection   | Requirement for branch protection from -1 to 10.        |
| -dw \| --dangerous-workflow   | Requirement for dangerous workflow from -1 to 10.        |
| -cr \| --code-review   | Requirement for code review from -1 to 10.        |
| -c \| --contributors   | Requirement for contributors from -1 to 10.        |
| -pd \| --pinned-dependencies   | Requirement for pinned dependencies from -1 to 10.        |
| -tp \| --token-permissions   | Requirement for token permissions from -1 to 10.        |
| -p \| --packaging   | Requirement for packaging from -1 to 10.        |
| -sr \| --signed-releases   | Requirement for signed releases from -1 to 10.        |
| -b \| --backend   | URL of the backend server. Defaults to internal docker backend.        |
| -o \| --output   | Format of the output. Can be table, simplified or JSON. Defaults to table.        |
| -v \| --verbose   | Print the output verbosely.        |
| --help   | Show the help page for the analyze command.        |


## SBOMs Command
This command prints out the names of all SBOMs in the database.

* Usage:
  ```
  docker compose run ossqa-cli sboms [OPTIONS…]
  ```
* Example:
  ```
  docker compose run ossqa-cli sboms -o json
  ```

### Options
| Option      | Description |
| ----------- | ----------- |
| -b \| --backend   | URL of the backend server. Defaults to internal docker backend.        |
| -o \| --output   | Format of the output. Can be table or json. Defaults to table.        |
| -v \| --verbose   | Print the output verbosely.        |
| --help   | Show the help page for the SBOMs command        |


## Lookup Command
This command prints out details of all SBOMs in the database that have a specified name.

* Usage:
  ```
  docker compose run ossqa-cli lookup [OPTIONS…] NAME
  ```
* Example:
  ```
  docker compose run ossqa-cli lookup -o table sysman
  ```

### Prepositionals
| Positionals      | Description |
| ----------- | ----------- |
| NAME      | Name of the SBOMs to print the details of.       |

### Options
| Option      | Description |
| ----------- | ----------- |
| -b \| --backend   | URL of the backend server. Defaults to internal docker backend.        |
| -o \| --output   | Format of the output. Can be table or json. Defaults to table.        |
| -v \| --verbose   | Print the output verbosely.        |
| --help   | Show the help page for the lookup command        |

## Contribute
This project is open source, contributions are appreciated. 

## Help

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](https://github.com/OSSQA-PUM/OSSQA/blob/main/LICENSE) file for details
