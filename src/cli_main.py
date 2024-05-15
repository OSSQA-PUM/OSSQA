"""
The entry point of the CLI.
"""
from main.frontend.cli import ossqa_cli


def main():
    """
    The main function of the CLI.

    This function creates the parser, parses the arguments, and runs the CLI.
    """
    ossqa_cli()


if __name__ == "__main__":
    main()
