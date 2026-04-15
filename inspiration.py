import requests
from colorama import Fore, Style

from helpers import ask_repeat, SEPERATOR_BIG, SEPERATOR_SMALL
from search_advice import advice_search_loop


def print_inspiration_menu():
    print(f"{SEPERATOR_BIG}\nThese are your options: \n"
          f"{SEPERATOR_SMALL}\n"
          f'{Fore.YELLOW}{Style.BRIGHT}1. Hear a ("good") joke\n'
          f"2. Get a famous quote\n"
          f"3. Get random advice slip\n"
          f"4. Search advice by a keyword\n"
          f"5. Back\n")

#--------------------- FALLBACK ----------------------
def fall_back(categorie):
    """
    Function for fallback advice, quote and joke in case None is returned in API functions.

    :param categorie: quote, advice, or joke. str
    :return: fallback message
    """
    fall_back_advice = '"Every journey begins with a single step."'
    fall_back_quote = ('"I learned that courage was not the absence of fear, but the triumph over it. '
                       'The brave man is not he who does not feel afraid, but he who conquers that fear."\n'
                       '- Nelson Mandela')
    fall_back_joke = ("What's a computer's favorite snack?\n"
                      "\n"
                      "Microchips")

    if categorie == 'advice':
        print_text = fall_back_advice
    if categorie == 'quote':
        print_text = fall_back_quote
    if categorie == 'joke':
        print_text = fall_back_joke

    print(f'{SEPERATOR_BIG}\n'
          f'Printing fallback {categorie}.\n'
          f'Your {categorie} for today is:\n'
          f'{SEPERATOR_SMALL}\n'
          f'{print_text}')


#--------------------- JOKE ----------------------
def get_joke():
    url = 'https://jokefather.com/api/jokes/random'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Something went wrong. Status code: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        return None


def display_joke(joke_data):
    """ Display joke with null check.
    If data is None - fallback joke will be printend.
    If data has a joke, the text is printed. If the data format gives an error - again fallback joke will be printed.
    """

    if joke_data is None:
        print(f'Unable to fetch new quote at this time.')
        fall_back("joke")
        return

    try:
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        print(f'{SEPERATOR_BIG}\n'
              f'Your joke for today is:\n'
              f'{SEPERATOR_SMALL}\n'
              f'{setup}\n'
              f'\n'
              f'{punchline}')

    except (KeyError, TypeError) as e:
        print(f'Unexpected response format. Error: {e}')
        fall_back("joke")


# -------------------- QUOTE -----------------------
def get_quote():
    """
    Fetch zen-quote from API. Returns None on failure.
    """
    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Something went wrong. Status code: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        return None


def display_quote(quote_data):
    """ Display quote with null check.
    If data is None - fallback quote will be printend.
    If data has quote, the text is printed. If the data format gives an error - again fallback quote will be printen.
    """

    if quote_data is None:
        print(f'Unable to fetch new quote at this time.')
        fall_back("quote")
        return

    try:
        quote_str = quote_data[0]["q"]
        author = quote_data[0]["a"]
        print(f'{SEPERATOR_BIG}\n'
              f'Your quote for today is:\n'
              f'{SEPERATOR_SMALL}\n'
              f'"{quote_str}"\n'
              f'- {author}')

    except (KeyError, TypeError) as e:
        print(f'Unexpected response format. Error: {e}')
        fall_back("quote")


#--------------------- ADVICE ----------------------
def get_advice():
    """Fetch advice from API. Returns None on failure."""
    url = 'https://api.adviceslip.com/advice'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Something went wrong. Status code: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        return None


def display_advice(advice_data):
    """ Display advice with null check.
    If data is None - fallback advice will be printend.
    If data has advice, the text is printed. If the data format gives an error - again fallback advice will be printen.
    """

    if advice_data is None:
        print(f'Unable to fetch new advice at this time.')
        fall_back("advice")
        return

    try:
        new_advice = advice_data['slip']['advice']
        print(f'{SEPERATOR_BIG}\n'
              f'Your advice for today is:\n'
              f'{SEPERATOR_SMALL}\n'
              f'"{new_advice}"')

    except (KeyError, TypeError) as e:
        print(f'Unexpected response format. Error: {e}')
        fall_back("advice")

#----------------------- MAIN LOOP INSPIRATION SUBMENU ----------------
def inspiration_loop():

    while True:
        print_inspiration_menu()

        try:
            choose_inspiration = int(input("Please choose an option: "))

            action_completed = False

            match choose_inspiration:
                case 1:
                    joke = get_joke()
                    display_joke(joke)
                    action_completed = True

                case 2:
                    quote = get_quote()
                    display_quote(quote)
                    action_completed = True

                case 3:
                    advice = get_advice()
                    display_advice(advice)
                    action_completed = True

                case 4:
                    advice_search_loop()
                    action_completed = True

                case 5:
                    return

                case _:
                    print(f'{Fore.RED}Invalid choice.{Fore.RESET} \nPlease choose between options 1 - 5. \n')

            if action_completed: # end menu cycle & action 1-4 done -- ask if user wants to repeat
                if not ask_repeat("1. Get some inspiration to start your day"):
                    return

        except ValueError as e:
            print(f"{Fore.RED}Invalid input{Fore.RESET} -- Error: {e}\n \n{Style.BRIGHT}Please enter a digit.\n")

