def ask_repeat(prompt = ""):
    """
    Ask if user wants to repeat the action
    :param prompt: str with the action to print
    :return: bool: True if want to go again. False if not want to continue
    """

    while True:
        again = input(f"\nDo you want to repeat the action: \033[4m{prompt}\033[0m? (y/n): ")
        if again in ['y', 'yes']:
            return True
        elif again in ['n', 'no']:
            return False
        else:
            print("\nInvalid input. Please enter 'y' or 'n'.")