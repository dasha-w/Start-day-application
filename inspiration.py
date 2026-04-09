import requests
from helpers import ask_repeat
from search_advice import advice_search_loop


def print_inspiration_menu():
    print(f"These are your options: \n"
          f"---------------------------\n"
          f'1. Hear a ("good") joke\n'
          f"2. Get a famous quote\n"
          f"3. Get some advice\n"
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

    print(f'Printing fallback {categorie}.\n'
          f'-------------------------\n'
          f'Your {categorie} for today is:\n'
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
        print(f'------------------------\n'
              f'Your joke for today is:\n'
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
        return None  # todo klopt dat? idem get_advice()


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
        print(f'------------------------\n'
              f'Your quote for today is:\n'
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
        print(f'------------------------\n'
              f'Your advice for today is:\n"{new_advice}"')

    except (KeyError, TypeError) as e:
        print(f'Unexpected response format. Error: {e}')
        fall_back("advice")

#----------------------- MAIN LOOP INSPIRATION SUBMENU ----------------
def inspiration_loop():

    while True:
        print_inspiration_menu()

        try:
            choose_inspiration = int(input("Please choose an option: "))

            match choose_inspiration:
                case 1:
                    joke = get_joke()
                    display_joke(joke)

                case 2:
                    quote = get_quote()
                    display_quote(quote)

                case 3:
                    advice = get_advice()
                    display_advice(advice)

                case 4:
                    advice_search_loop()

                case 5:
                    return

                case _:
                    print(f'\033[31mInvalid choice.\033[0m Please choose between options 1 - 4. ')

            if not ask_repeat("1. Get some inspiration to start your day"): # end menu cycle - ask if want to repeat
                return

        except ValueError as e:
            print(f"\033[31mInvalid input\033[0m - error: {e} \nPlease enter a digit.\n")

