"""
The entry point of the CLI.
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
