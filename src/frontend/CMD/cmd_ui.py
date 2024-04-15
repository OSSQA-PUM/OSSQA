"""
This module is the command line interface for the SBOM search tool.
"""
import glob
import os
from pathlib import Path
from tabulate import tabulate
import requests
#import util
#import frontend_api


def get_choice():
    """
    Helper to get user input

    Returns:
        str: the user's choice
    """
    choice = input("Select: ")
    return choice.strip()


def display_ui():
    """
    Helper to display the main menu

    Returns:
        None
    """
    print("What would you like to do?")
    print("1. Select SBOM")
    print("2. Search selected SBOM")
    print("3. Set token")
    print("4. Exit")


def clear_console():
    """
    Helper to clear the console

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def set_token():
    """
    Helper to set the token

    Returns:
        None
    """
    print("Set a token:")
    os.environ['GITHUB_AUTH_TOKEN'] = input("Input your token: ")
    if False:
    #if not util.check_token_usage():
        os.environ['GITHUB_AUTH_TOKEN'] = ""
        print("Token was invalid")


def select_sbom() -> str:
    """
    Function for selecting the SBOM
    Returns:
        str: the path to the selected SBOM
    """
    clear_console()
    print("Please select the SBOM to be searched \n")
    #Finds the SBOMS that the user has
    sboms = list(list(glob.glob(str(Path(__file__).parent.absolute() / 'example-SBOM.json'))))
    for i, sbom in enumerate(sboms):
        print(f"{i}: {sbom}")
    choice = "not valid"
    while not choice.isdigit():
        choice = get_choice()
    #Checks that the choice is valid
    if int(choice) < 0 or int(choice) > len(sboms):
        print("Invalid choice")
        return select_sbom()
    selected_sbom = sboms[int(choice)]
    clear_console()
    print(f"SBOM selected to be searched: {selected_sbom}")
    return selected_sbom


def search_sbom(sbom):
    """
    Function for searching the selected SBOM
    Args:
        sbom (str): the path to the selected SBOM
    
    Returns:
        None
    """
    dict_weighted_results: list[(str, int, str)] #(checkname, score, dependency)
    #dict_weighted_results = frontend_api.frontend_api(sbom)
    result = requests.post("http://localhost:98/analyze", sbom)
    dict_weighted_results = result.json()
    print(tabulate(dict_weighted_results,
                   headers=["Checkname", "Score", "Dependency"]))


def main():
    """
    Main function of the program

    Returns:
        None
    """
    sbom = ""

    while True:
        display_ui()
        user_choice = get_choice()

        if user_choice == "1":
            sbom = select_sbom()

        elif user_choice == "2":
            if not os.environ.get('GITHUB_AUTH_TOKEN'):
                print("No token selected. Please select one and try again")
                continue

            if not sbom:
                print("No SBOM selected. Please select one and try again")
                continue

            search_sbom(sbom)

        elif user_choice == "3":
            clear_console()
            set_token()

        elif user_choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose again.")


def search_files():
    """
    Function for searching the selected SBOM
    Args:
        sbom (str): the path to the selected SBOM

    Returns:
        None
    """
    files = [f for f in glob.glob("*.txt")]
    print(files)
    return files


if __name__ == "__main__":
    main()
