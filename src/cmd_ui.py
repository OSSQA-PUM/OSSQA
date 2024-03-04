
import glob
import os


from src import util
from src import frontend_api

def get_choice():
    choice = input("Select: ")
    return choice.strip()


def display_ui():
    print("What would you like to do?")
    print("1. Select SBOM")
    print("2. Search selected SBOM")
    print("3. Set token")
    print("4. Exit")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_tokens():
    print("Choose a token:")
    files = search_files()
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files


def set_token():
    print("Set a token:")
    os.environ['GITHUB_AUTH_TOKEN'] = input("Input your token: ")
    if not util.check_token_usage():
        os.environ['GITHUB_AUTH_TOKEN'] = ""
        print("Token was invalid")


def select_sbom():
    clear_console()
    print("Please select the SBOM to be searched \n")
    sboms = [f for f in glob.glob("src/*.json")]
    for i, sbom in enumerate(sboms):
        print(f"{i}: {sbom}")
    choice = get_choice()
    if int(choice) < 0 or int(choice) > len(sboms):
        print("Invalid choice")
        return
    
    selected_sbom = sboms[int(choice)]
    
    clear_console()
    print(f"SBOM selected to be searched: {selected_sbom}")
    return selected_sbom


def search_sbom(sbom):
    print(sbom)
    dict_weighted_results = frontend_api.frontend_api(sbom)
    

def make_choice(choice: int) -> None:
    if choice == "1": # Search SBOM
        pass


def main():
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
    files = [f for f in glob.glob("*.txt")]
    print(files)
    return files


if __name__ == "__main__":
    main()

#EOF end of file