import sys
from colorama import init, Fore, Style
from helpers import SEPERATOR_BIG, SEPERATOR_SMALL
from inspiration import inspiration_loop
from weather import weather_loop

init(autoreset=True)

def print_intro():
    print(f'{SEPERATOR_BIG}\n'
          f'\n{Fore.MAGENTA}{Style.BRIGHT}Good morning! \nWelcome to the start-day application!{Style.RESET_ALL}\n'
          f'\nThis application is here to help you get a good start to your day.\n'
          f"Please pause and reflect on how you're feeling before you continue.\n")


def print_main_menu():
    print(f'{SEPERATOR_BIG}\n'
          f'What would you like to do?\n'
          f'{SEPERATOR_SMALL}\n'
          f'{Fore.CYAN}{Style.BRIGHT}1. Get some inspiration to start your day\n'
          f'2. Get the weather forecast\n'
          f"3. Quit the program\n")


def exit_application():
    print(f'\n{SEPERATOR_BIG}\n'
          f'Thank you for using the start-day application.\n'
          f"\nDon't forget the advice and/or inspiration you've received today.\n"
          f"\n{Fore.MAGENTA}Have a wonderful day!{Fore.RESET}\n{SEPERATOR_SMALL}")
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
                print(f'{Fore.RED}Invalid choice.{Fore.RESET} \nPlease choose between options 1 - 3. \n')

        except ValueError as e:
            print(f"{Fore.RED}Invalid input{Fore.RESET} -- Error: {e}\n \n{Style.BRIGHT}Please enter a digit.\n")


if __name__ == "__main__":
    main()


#todo type hints in functions

