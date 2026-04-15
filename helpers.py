import datetime as dt
from colorama import Fore, Style

DEGREE_SYMBOL = chr(176)
SEPERATOR_BIG = ('='*80)
SEPERATOR_SMALL = ('-'*80)


def ask_repeat(prompt = ""):
    """
    Ask if user wants to repeat the action
    :param prompt: str with the action to print
    :return: bool: True if want to go again. False if not want to continue
    """

    while True:
        again = input(f"\nDo you want to repeat the action: {Fore.BLUE}{prompt}{Fore.RESET}? (y/n): ").strip().lower()
        if again in ['y', 'yes']:
            return True
        elif again in ['n', 'no']:
            return False
        else:
            print(f"\n{Fore.RED}Invalid input.{Fore.RESET} Please enter 'y' or 'n'.")


def parse_date(date: str):

    try:

        date_to_dt = dt.date.fromisoformat(date)
        date_format = dt.date.strftime(date_to_dt, "%A %d %B %Y")

        return date_format

    except (TypeError, ValueError) as e:
        print(f'Wrong input when parsing date. {Fore.RED}Error:{Fore.RESET} {e}\nUsing original date format.')
        return date

