"""
Module for searching advice slips by keyword using AdviceSlip API.
Handles search logic, parsing, and user interaction for browsing results.
"""

import requests
from colorama import Fore, Style

from helpers import ask_repeat, SEPERATOR_BIG, SEPERATOR_SMALL, validate_input


#--------------------- SEARCH ADVICE ----------------------
def search_advice(keyword: str)-> dict | None:
    """
    Search for advice slips by keyword via API.

    :param keyword: the word to search for
    :return: dict | None: JSON data or None on failure
    """
    url = f"https://api.adviceslip.com/advice/search/{keyword}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED}Something went wrong.{Fore.RESET} Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error {e}")
        return None


#--------------------- PARSE ADVICE RESPONSE ----------------------
def parse_api_advice_response(api_data: dict | None) -> dict:
    """
       Normalize inconsistent API response of advice slip into standard format.

       :param api_data: raw JSON from API | None
       :return: dict: {"found": bool, "slips": list, "error": str | None}
       """
    result = {"found": False, "slips": [], "error": None} # type: dict[str, bool | list | str | None]

    if api_data is None:
        result["error"] = "No data received from API"

    elif "message" in api_data:
        result["error"] = api_data["message"]["text"]

    elif "slips" in api_data:
        result["found"] = True
        result["slips"] = api_data["slips"]

    else:
        print(f"Unexpected API response structure: {api_data}")
        result["error"] = "Unexpected API response structure"

    return result


#--------------------- DISPLAY AND CHOOSE FROM NUMBER OF ADVICE SLIPS FOUND ----------------------
def display_number_results(count: int)-> None:
    """
    display the number of advice slips (results) found with the keyword
    """
    print(f"\n> Found {count} advice slip(s). ")


def choose_advice(total_count: int)-> int:
    """
    Ask the user to choose an advice slip number from the total number of results.
    Function validates if the number is within range
    :param total_count: Total nymber of slips found
    :return: int: index (0-based)
    """

    while True:
        try:
            choice = int(input(f"{SEPERATOR_SMALL}\n"
                               f"Choose a number between 1 - {total_count} to display a found advice slip: "))

            #Check if within range
            if 1 <= choice <= total_count:
                return choice - 1 # convert to 0 index
            else:
                print(f"\nPlease enter a number between 1 and {total_count}")

        except ValueError:
            print(f"\n{Fore.RED}Invalid input.{Fore.RESET} \nPlease enter a whole number.")


#--------------------- DISPLAY CHOSEN ADVICE  ----------------------
def display_chosen_advice(data: list, index: int)-> None:
    """
    Display the specific advice slip from the chosen index
    :param data: list of advice slips from parsed dictionary
    :param index: Index number of slip to display
    """
    try:
        advice = data[index]["advice"]
        print(f"\n{SEPERATOR_BIG}\n"
              f"Your advice for today is:\n"
              f'{SEPERATOR_SMALL}\n"{advice}"')

    except (KeyError, TypeError) as e:
        print(f"Unexpected response format. {Fore.RED}Error: {e}")


def browse_slips(slips: list) -> None:
    """
    Allow user to browse multiple slips if more than 1 is found

    :param slips: list of found advice slips
    """

    total_count = len(slips)

    if total_count == 1:  # if there is only one advice found - no choice and advice is printed
        print(f"Printing found advice slip.\n")
        display_chosen_advice(slips, 0)
        return

    while True:
        chosen = choose_advice(total_count)  # Let user choose a number to display advice
        display_chosen_advice(slips, chosen)

        while True:
            again = input(
                f"\n{Fore.YELLOW}{Style.BRIGHT}Would you like to see another advice slip of "
                f"the {total_count} found? (y/n): "
            ).lower().strip()

            if not validate_input(again, "yn"): # validates input to only y/n
                print(f"\n{Fore.RED}Invalid input.{Fore.RESET} Please enter 'y' or 'n'.")

            if again in ["y", "yes"]:
                break # breaks again while loop and goes back to choose_advice
            elif again in ["n", "no"]:
                return # ends function



#--------------------- RUN ADVICE SEARCH  ----------------------
def run_advice_search() -> bool:
    """
    Function handles 1 search for advice slips
        input keyword -> fetch data -> parse data -> display
            & browse slips if more than 1
    :return: bool - True if search completed successfully or user quit
        False if search unsuccessful.
    """

    print(f"\n===== SEARCH for ADVICE =====\n")
    keyword = input(f'You are about to search for advice based on a keyword (e.g. "life", "happiness").\n{SEPERATOR_SMALL}\n'
                    "What keyword do you want to search for? (q to quit search): ").lower()

    if not keyword:
        print(f"\n{Fore.RED}Keyword cannot be empty.{Fore.RESET}\n{SEPERATOR_SMALL}")
        return False

    if not validate_input(keyword, "advice_search"):
        print(f'\n{Fore.RED}Invalid character input.{Fore.RESET} '
              f'Please only enter letters, digits, a space, hyphen, or apostrophe.')
        return False

    if keyword == "q":
        return True

    # get api data
    api_data = search_advice(keyword)

    # parse api data
    parsed = parse_api_advice_response(api_data)

    # If no advice found with keyword
    if not parsed["found"]:  # if not False --> True | If not True --> False
        print(f"\n{Fore.RED}No advice found:{Fore.RESET} {parsed["error"]}\n")
        return False

    # if there is advice found for the keyword
    slips = parsed["slips"]

    # display number of slips found
    display_number_results(len(slips))

    # Show slips
    browse_slips(slips)
    return True


def advice_search_loop() -> None:
    """ Loop for repeated advice searches """
    while True:
        search_completed = run_advice_search()

        if search_completed:
            if not ask_repeat("4. Search advice by a keyword"):
                return

