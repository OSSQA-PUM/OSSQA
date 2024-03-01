"""Test for Docker

This file is used as a test file for running python in Docker.
"""
import os
import numpy as np # Notice that numpy may not be is not installed on your local machine,
#but it will be installed in the docker container since it is declared in the requirements.txt file



def do_something():
    """Example code to test docker container."""
    print("Goodbye World!")
    print("Hello World!")
    print(os.path.dirname(os.path.abspath(__file__)))

    a = np.arange(15).reshape(3, 5)

    print(a)


def main():
    """Main function of the program"""
    do_something()

if __name__ == "__main__":
    main()
