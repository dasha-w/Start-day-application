import sys
from colorama import init, Fore, Style
from helpers import SEPARATOR_BIG, SEPARATOR_SMALL, print_menu, MENU_OPTIONS
from inspiration import inspiration_loop

try:
    from config import WEATHER_API_KEY

    if not WEATHER_API_KEY:
        print(f"{Fore.RED}Error:{Fore.RESET} WEATHER_API_KEY is empty in config.py")
        sys.exit(1)
except (ImportError, ValueError) as e:
    print(f"{Fore.RED}Setup error:{Fore.RESET} {e}.")
    print(f"Please create config.py and add your API Key. See README.md")
    sys.exit(1)

from weather import weather_loop

init(autoreset=True) # colorama initialisation. autoreset - resets style and colors at end of each print

def print_intro():
    print(f"{SEPARATOR_BIG}\n"
          f"\n{Fore.MAGENTA}{Style.BRIGHT}Good morning! \nWelcome to the start-day application!{Style.RESET_ALL}\n"
          f"\nThis application is here to help you get a good start to your day.\n"
          f"Please pause and reflect on how you're feeling before you continue.\n")


def exit_application():
    print(f"\n{SEPARATOR_BIG}\n"
          f"Thank you for using the start-day application.\n"
          f"\nDon't forget the advice and/or inspiration you've received today.\n"
          f"\n{Fore.MAGENTA}Have a wonderful day!{Fore.RESET}\n{SEPARATOR_SMALL}")
    sys.exit(0)


def main():
    print_intro()

    while True:
        print_menu("main")

        try:
            max_option = len(MENU_OPTIONS["main"]["options"])
            choose_main = int(input("Please choose an option: "))

            if choose_main == 1:
                print("\nGreat!")
                inspiration_loop()

            elif choose_main == 2:
                weather_loop()

            elif choose_main == 3:
                exit_application()

            else:
                print(f"{Fore.RED}Invalid choice.{Fore.RESET} Please choose between options 1 - {max_option}. \n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid input{Fore.RESET} -- Error: {e}\n \n{Style.BRIGHT}Please enter a digit.\n")


if __name__ == "__main__":
    main()
