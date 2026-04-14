import sys

from helpers import SEPERATOR_BIG, SEPERATOR_SMALL
from inspiration import inspiration_loop
from weather import weather_loop


def print_intro():
    print(f'{SEPERATOR_BIG}\n'
          f'\n\u001b[35;1mGood morning! \nWelcome to the start-day application!\u001b[0m\n'
          f'\nThis application is here to help you get a good start to your day.\n'
          f"Please pause and reflect on how you're feeling before you continue.\n")


def print_main_menu():
    print(f'{SEPERATOR_BIG}\n'
          f'What would you like to do?\n'
          f'{SEPERATOR_SMALL}\n'
          f'\u001b[36;1m1. Get some inspiration to start your day\n'
          f'2. Get the weather forecast\n'
          f"3. Quit the program\n\u001b[0m")


def exit_application():
    print(f'\n{SEPERATOR_BIG}\n'
          f'Thank you for using the start-day application.\n'
          f"Don't forget the advice and/or inspiration you've received today.\n"
          f"\u001b[35;1mHave a wonderful day!\u001b[0m")
    sys.exit(0)


def main():
    print_intro()

    while True:
        print_main_menu()

        try:
            choose_main = int(input("Please choose an option: "))

            if choose_main == 1:
                print(f'\nGreat!')
                inspiration_loop()

            elif choose_main ==2:
                weather_loop()

            elif choose_main == 3:
                exit_application()

            else:
                print(f'\033[31mInvalid choice.\033[0m \nPlease choose between options 1 - 3. \n')

        except ValueError as e:
            print(f"\033[31mInvalid input\033[0m - error: {e} \nPlease enter a digit.\n")


if __name__ == "__main__":
    main()

#todo u001 vs 003
#todo repeat na fout invoer bij inspo en weather menu -- inspo done