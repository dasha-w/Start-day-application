"""
Module for fetching and displaying inspirational content (joke, quote, advice).
External API: JokeFather, ZenQuotes, AdviceSlip
"""
import time

import requests
from colorama import Fore, Style

from helpers import ask_repeat, SEPARATOR_BIG, SEPARATOR_SMALL, MENU_OPTIONS, print_menu
from search_advice import advice_search_loop


#--------------------- FALLBACK ----------------------
def fall_back(categorie: str) -> None:
    """
    Display hardcoded fallback advice, quote and joke in case API call fails
    (if API fails, API functions returns None)

    :param
        categorie (str): quote, advice, or joke
    """
    fallback = {
        "advice": '"Every journey begins with a single step."',
        "quote": (
            '"I learned that courage was not the absence of fear, but the triumph over it. '
            'The brave man is not he who does not feel afraid, but he who conquers that fear."\n'
            "- Nelson Mandela"
            ),
        "joke": "What's a computer's favorite snack?\n\nMicrochips"
    }

    print_text = fallback.get(categorie)

    print(f"{SEPARATOR_BIG}\n"
          f"Printing fallback {categorie}\n"
          f"Your {categorie} for today is:\n"
          f"{SEPARATOR_SMALL}\n"
          f"{print_text}")


#---------------------- API -----------------------
def get_api_data(categorie: str) -> dict | None:
    """
    Fetch API data
    :param categorie: Type of content to fetch (advice, quote, joke)
    :return:
        dict | None: JSON response or None on failure.
    """
    urls = {
        "advice": "https://api.adviceslip.com/advice",
        "quote": "https://zenquotes.io/api/random",
        "joke": "https://jokefather.com/api/jokes/random"
    }

    url = urls.get(categorie)

    if url is None:
        print(f"{Fore.RED}Incorrect categorie parameter.{Fore.RESET} "
              f"Categorie needs to be 'advice', 'quote', or 'joke'.")
        return None  # exit before url is used

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Something went wrong. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error {e}")
        return None


#--------------------- JOKE ----------------------
def display_joke(joke_data: dict | None) -> None:
    """
    Display joke with error handling and fallback.
        If data is None - fallback joke will be printend.
        If data has a joke, the API is parsed and text is printed.
        If the data format gives an error - again fallback joke will be printed.
    :param joke_data: dict | None: JSON data from API
    """

    if joke_data is None: # no url specified, try api failed, or statuscode != 200
        print(f"Unable to fetch new quote at this time.")
        fall_back("joke")
        return

    try:
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        print(f"{SEPARATOR_BIG}\n"
              f"Your joke for today is:\n"
              f"{SEPARATOR_SMALL}\n"
              f"{setup}\n")
        time.sleep(2.5)
        print(f"{punchline}")

    except (KeyError, TypeError) as e:
        print(f"Unexpected response format. Error: {e}")
        fall_back("joke")


# -------------------- QUOTE -----------------------
def display_quote(quote_data: list | None) -> None:
    """
    Display quote with error handling and fallback.
        If data is None - fallback quote will be printend.
        If data has quote, the data is parsed, and text is printed.
        If the data format gives an error - again fallback quote will be printen.
    :param: quote_data (list | None): JSON data from API
    """

    if quote_data is None:
        print(f"Unable to fetch new quote at this time.")
        fall_back("quote")
        return

    try:
        quote_str = quote_data[0]["q"]
        author = quote_data[0]["a"]
        print(f"{SEPARATOR_BIG}\n"
              f"Your quote for today is:\n"
              f"{SEPARATOR_SMALL}\n"
              f'"{quote_str}"\n'
              f"- {author}")

    except (KeyError, TypeError) as e:
        print(f"Unexpected response format. Error: {e}")
        fall_back("quote")


#--------------------- ADVICE ----------------------
def display_advice(advice_data: dict | None) -> None:
    """
    Display advice with error handling and fallback.
        If data is None - fallback advice will be printend.
        If data has advice, the data is parsed, and text is printed.
        If the data format gives an error - again fallback advice will be printen.
    :param advice_data: JSON data from API
    """

    if advice_data is None:
        print(f"Unable to fetch new advice at this time.")
        fall_back("advice")
        return

    try:
        new_advice = advice_data["slip"]["advice"]
        print(f"{SEPARATOR_BIG}\n"
              f"Your advice for today is:\n"
              f"{SEPARATOR_SMALL}\n"
              f'"{new_advice}"')

    except (KeyError, TypeError) as e:
        print(f"Unexpected response format. Error: {e}")
        fall_back("advice")


# ----------------------- MAIN LOOP INSPIRATION SUBMENU ----------------
def inspiration_loop():
    """Main loop for the inspiration submenu"""

    while True:
        print_menu("inspiration")

        try:
            choose_inspiration = int(input("Please choose an option: "))
            max_option = len(MENU_OPTIONS["inspiration"]["options"])
            action_completed = False

            match choose_inspiration:
                case 1:
                    joke = get_api_data("joke")
                    display_joke(joke)
                    action_completed = True

                case 2:
                    quote = get_api_data("quote")
                    display_quote(quote)
                    action_completed = True

                case 3:
                    advice = get_api_data("advice")
                    display_advice(advice)
                    action_completed = True

                case 4:
                    advice_search_loop()
                    action_completed = True

                case 5:
                    return

                case _:
                    print(f"{Fore.RED}Invalid choice.{Fore.RESET} Please choose between options 1 - {max_option}. \n")

            if action_completed: # end menu cycle & action 1-4 done -- ask if user wants to repeat
                if not ask_repeat("1. Get some inspiration to start your day"):
                    return

        except ValueError as e:
            print(f"{Fore.RED}Invalid input{Fore.RESET} -- Error: {e}\n \n{Style.BRIGHT}Please enter a digit.\n")

