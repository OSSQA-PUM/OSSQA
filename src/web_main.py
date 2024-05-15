"""
This module serves as the entry point for running the web application.

It imports the `run` function from the `main.frontend.web_api`
module and calls it when the script is executed.

This module is used by the docker-compose file to start the web application.

Usage:
    python web_main.py
"""
from main.frontend.web_api import run


if __name__ == "__main__":
    run()
