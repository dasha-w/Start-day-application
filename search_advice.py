import requests
from helpers import ask_repeat

#--------------------- SEARCH ADVICE ----------------------
def search_advice(keyword):
    """
    api request for search advice slips endpoint
    :param keyword: the word to search for
    :return: json or None
    """
    url = f'https://api.adviceslip.com/advice/search/{keyword}'

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


#--------------------- PARSE ADVICE RESPONSE ----------------------
def parse_api_advice_response(api_data):
    """
       Normalize inconsistent API response of advice slip into standard format.

       :param api_data: from advice api
       :return: {'found: bool, 'slips': list, 'error': str or None}
       """
    result = {'found': False, 'slips': [], 'error': None}

    if api_data is None:
        result['error'] = 'No data received from API'

    if 'message' in api_data:
        result['error'] = api_data['message']['text']

    if 'slips' in api_data:
        result['found'] = True
        result['slips'] = api_data['slips']

    return result


#--------------------- DISPLAY AND CHOOSE FROM NUMBER OF ADVICE SLIPS FOUND ----------------------
def display_number_results(count):
    """
    display the number of advice slips found with the keyword
    :return: print statement
    """
    print(f'\nFound {count} advice slips. ')


def choose_advice(total_count):
    """
    Ask the user to choose an advice slip number.
    Function validates if the number is within range
    :param total_count: length of slips
    :return: index (0-based)
    """

    while True:
        try:
            choice = int(input(f'\nChoose a number between 1 - {total_count} to display a found advice slip: '))

            #Check if within range
            if 1 <= choice <= total_count:
                return choice - 1 # convert to 0 index
            else:
                print(f'\nPlease enter a number between 1 and {total_count}')

        except ValueError:
            print('\nInvalid input. Please enter a whole number.')


#--------------------- DISPLAY CHOSEN ADVICE  ----------------------
def display_chosen_advice(data, index):
    """
    Display the found advice slip from the chosen index
    :param data: list of advice slips from parsed dictionary
    :param index: the chosen number converted to 0-index
    :return: printed advice
    """
    try:
        advice = data[index]['advice']
        print(f'\n------------------------\n'
              f'Your advice for today is:\n"{advice}"')

    except (KeyError, TypeError) as e:
        print(f'Unexpected response format. Error: {e}')


def browse_slips(slips):
    """
    Let the user see the slips and choose to display multiple slips if more than 1 was found.
    :param slips: list of found slips
    :return: display chosen result while True or None when False.
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
            again = input(f"\nWould you like to see another slip of the {total_count} found? (y/n): ").lower().strip()
            if again in ['y', 'yes']:
                break
            elif again in ['n', 'no']:
                return
            else:
                print("Please enter 'y' or 'n'.")


#--------------------- RUN ADVICE SEARCH  ----------------------
def run_advice_search():
    """
       Handles 1 search for advice slips
       - asking for keyword
       - fetching data from api
       - parses data
       - browses results (one or more)

       :return:
       """
    print("\n ----- Search for Advice -----\n")
    keyword = input("You are about to search for advice based on a keyword (e.g. 'life', 'happiness').\n"
                    "What keyword do you want to search for?: ").lower()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    # get api data
    api_data = search_advice(keyword)

    # parse api data
    parsed = parse_api_advice_response(api_data)

    # If no advice found with keyword
    if not parsed['found']:  # if not False = True | If not True = False
        print(f'No advice found: {parsed['error']}')
        return

    # if there is advice found for the keyword
    slips = parsed['slips']

    # display number of slips found
    display_number_results(len(slips))

    # Show slips
    browse_slips(slips)


def advice_search_loop():
    """
    Handles search for advice slips with a keyword in a loop.
    :return:
    """
    while True:
        run_advice_search()

        if not ask_repeat("4. Search advice by a keyword"):
            return

