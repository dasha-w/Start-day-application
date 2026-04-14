import datetime as dt

DEGREE_SYMBOL = chr(176)
SEPERATOR_BIG = ('='*60)
SEPERATOR_SMALL = ('-'*60)


def ask_repeat(prompt = ""):
    """
    Ask if user wants to repeat the action
    :param prompt: str with the action to print
    :return: bool: True if want to go again. False if not want to continue
    """

    while True:
        again = input(f"\n\u001b[34mDo you want to repeat the action: \033[4m{prompt}\033[0m? (y/n): \u001b[0m")
        if again in ['y', 'yes']:
            return True
        elif again in ['n', 'no']:
            return False
        else:
            print("\nInvalid input. Please enter 'y' or 'n'.")


def parse_date(date: str):

    try:

        date_to_dt = dt.date.fromisoformat(date)
        date_format = dt.date.strftime(date_to_dt, "%A %d %B %Y")

        return date_format

    except (TypeError, ValueError) as e:
        print(f'Wrong input when parsing date. Error: {e}\nUsing original date format.')
        return date

