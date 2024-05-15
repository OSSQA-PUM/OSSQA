"""
The entry point of the CLI.

Example usage:
    python cli_main.py -a -p ../sboms/example-SBOM.json -g [YOUR_GIT_TOKEN]
"""
from main.frontend.cli import ossqa_cli


if __name__ == "__main__":
    ossqa_cli()
