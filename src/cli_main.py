"""
The entry point of the CLI.

Example usage: 
    python cli_main.py -a -p tests/main/unit/sboms/example-SBOM.json -g [YOUR_GIT_TOKEN]
"""

from main.frontend.cli import run_cli

def main():
    """
    The main function of the CLI.

    This function creates the parser, parses the arguments, and runs the CLI.
    """
    run_cli()

if __name__ == "__main__":
    main()
