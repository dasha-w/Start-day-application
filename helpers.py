"""
Helper utilities for the Start-Day Application.
Contains constants and functions for date parsing, user input validation
"""

import datetime as dt
import re
from colorama import Fore, Style

# Constants for terminal formatting
DEGREE_SYMBOL = chr(176)
SEPERATOR_BIG = ('='*80)
SEPERATOR_SMALL = ('-'*80)

MENU_OPTIONS = {
    "main": {
        "color": Fore.CYAN,
        "options": [
            "Get some inspiration to start your day",
            "Get the weather forecast",
            "Quit the program"
            ]
    },
    "inspiration": {
        "color": Fore.YELLOW,
        "options": [
            'Hear a ("good") joke',
            "Get a famous quote",
            "Get a random advice slip",
            "Search for advice by a keyword",
            "Back"
        ]
    },
    "weather":{
        "color": Fore.BLUE,
        "options": [
            "Get the current weather conditions",
            "Get the weather forecast for today",
            "Get clothing advice for today's weather forecast",
            "Back"
        ]
    }
}


def ask_repeat(prompt: str = "") -> bool:
    """
    Ask if user wants to repeat the action

    :param:
        prompt: str with the action to be repeated & printed in input
    :return:
        bool: True if user wants to repeat. False if user does not want to continue
    """

    while True:
        again = input(f"\nDo you want to repeat the action: {Fore.BLUE}{prompt}{Fore.RESET}? (y/n): ").strip().lower()

        if not validate_input(again, "yn"):
            print(f"\n{Fore.RED}Invalid input.{Fore.RESET} Please enter 'y' or 'n'.")

        if again in ["y", "yes"]:
            return True
        elif again in ["n", "no"]:
            return False



def parse_date(date: str) -> str:
    """
    Parse an ISO format date string to another format -> e.g. Monday 1 January 2020
    :param
        date: Date string in ISO format (YYYY-MM-DD)
    :return:
        str: formated date string. Returns original string if parsing fails.
    """
    try:

        date_to_dt = dt.date.fromisoformat(date)
        date_format = dt.date.strftime(date_to_dt, "%A %d %B %Y")

        return date_format

    except (TypeError, ValueError) as e:
        print(f"Wrong input when parsing date. {Fore.RED}Error:{Fore.RESET} {e}\nUsing original date format.")
        return date


def print_menu(menu_name: str):
    """
    Prints a formated menu with specific coloring based on menu_name key

    :param:
        menu_name (str): key from MENU_OPTIONS dict
    """

    if menu_name not in MENU_OPTIONS:
        print(f"{Fore.RED}Error:{Fore.RESET} {menu_name} not found.")

    menu_data = MENU_OPTIONS[menu_name]
    color = menu_data['color']
    options = menu_data['options']

    print(f"{SEPERATOR_BIG}\nWhat would you like to do?\n{SEPERATOR_SMALL}")

    # loop through menu options and print with numbering and specific color
    for i, option in enumerate(options,1):
        print(f"{color}{Style.BRIGHT}{i}. {option}")

    print("") # empty line after menu


def validate_input(input_string, pattern_type = "alphanumeric"):
    """
    Validate input based on pattern type.
    :param input_string: str - input to validate
    :param pattern_type: str - 'alphanumeric', 'city', 'digits','yn', 'advice_search'
    :return: bool
    """

    patterns = {
        "alphanumeric": r"^[a-zA-Z0-9]+$",
        "advice_search": r"^[a-zA-Z0-9\s\-']", # letters, digits, space, - and '
        "city": r"^[a-zA-Z\s\-']+$", #letters, space, - and '
        "yn": r"^[y|yes|n|no]$" # for yes/no input options
    }

    if not input_string:
        return False

    pattern = patterns.get(pattern_type, patterns["alphanumeric"])
    return bool(re.match(pattern, input_string))

