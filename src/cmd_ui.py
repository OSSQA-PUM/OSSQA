
import glob
import os
from pathlib import Path

import util
import frontend_api


def get_choice():
    """
    Helper to get user input
    """
    choice = input("Select: ")
    return choice.strip()


def display_ui():
    """
    Helper to display the main menu
    """
    print("What would you like to do?")
    print("1. Select SBOM")
    print("2. Search selected SBOM")
    print("3. Set token")
    print("4. Exit")


def clear_console():
    """
    Helper to clear the console
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def set_token():
    """
    Set GitHub token
    """
    print("Set a token:")
    os.environ['GITHUB_AUTH_TOKEN'] = input("Input your token: ")
    if not util.check_token_usage():
        os.environ['GITHUB_AUTH_TOKEN'] = ""
        print("Token was invalid")


def select_sbom() -> str:
    """
    Function for selecting an SBOM that the user has downloaded
    Returns:
        str: the path to the selected SBOM
    """
    clear_console()
    print("Please select the SBOM to be searched \n")
    #Finds the SBOMS that the user has
    sboms = list(list(glob.glob(str(Path(__file__).parent.absolute()\
                                / 'tests' / 'sboms' / 'example-SBOM.json'))))
    for i, sbom in enumerate(sboms):
        print(f"{i}: {sbom}")
    choice = get_choice()
    #Checks that the choice is valid
    if int(choice) < 0 or int(choice) > len(sboms):
        print("Invalid choice")
        return
    selected_sbom = sboms[int(choice)]
    clear_console()
    print(f"SBOM selected to be searched: {selected_sbom}")
    return selected_sbom


def search_sbom(sbom):
    """
    Searches the SBOM through the Frontend API
    """
    dict_weighted_results = frontend_api.frontend_api(sbom)
    print(dict_weighted_results)


def main():
    """
    TODO: add docstring
    """
    while True:
        display_ui()
        user_choice = get_choice()

        if user_choice == "1":
            sbom = select_sbom()

        elif user_choice == "2":
            if not os.environ.get('GITHUB_AUTH_TOKEN') or not sbom:
                print("No token or SBOM selected. Please select one and try again")
                break
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
    TODO: add doctring
    """
    files = [f for f in glob.glob("*.txt")]
    print(files)
    return files


if __name__ == "__main__":
    main()

#EOF end of file