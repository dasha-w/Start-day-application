import sys
from inspiration import inspiration_loop
from weather import weather_loop


def print_intro():
    print(f'----------------------------------------------------------\n'
          f'Good morning! \nWelcome to the start-day application!\n'
          f'\nThis application is here to help you get a good start to your day.\n'
          f"Please pause and reflect on how you're feeling before you continue.\n")


def print_main_menu():
    print(f'What would you like to do?\n'
          f'---------------------------------------\n'
          f'1. Get some inspiration to start your day\n'
          f'2. Get the weather forecast\n'
          f"3. Quit the program\n")


def exit_application():
    print(f'\nThank you for using the start-day application.\n'
          f"Don't forget the advice and/or inspiration you've received today.\n"
          f"Have a wonderful day!")
    sys.exit(0)


def main():
    print_intro()

    while True:
        print_main_menu()

        try:
            choose_main = int(input("Please choose an option: "))

            if choose_main == 1:
                print(f'\nGreat!\n')
                inspiration_loop()

            elif choose_main ==2:
                weather_loop()

            elif choose_main == 3:
                exit_application()

            else:
                print(f'\033[31mInvalid choice.\033[0m Please choose between options 1 - 4. \n')

        except ValueError as e:
            print(f"\033[31mInvalid input\033[0m - error: {e} \nPlease enter a digit.\n")


if __name__ == "__main__":
    main()