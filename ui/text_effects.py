def print_typing_effect(text, delay=0.05):
    """
    Prints text with a typing effect.
    
    Args:
        text (str): The text to print.
        delay (float): The delay between each character.
    """
    import sys
    import time

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Ensure the cursor moves to the next line after printing the text

def print_bold(text):
    """
    Prints text in bold.
    
    Args:
        text (str): The text to print in bold.
    """
    print(f"\033[1m{text}\033[0m")  # ANSI escape codes for bold text

def print_italic(text):
    """
    Prints text in italic.
    
    Args:
        text (str): The text to print in italic.
    """
    print(f"\033[3m{text}\033[0m")  # ANSI escape codes for italic text

def print_coloured(text, color):
    """
    Prints text in a specified color.
    
    Args:
        text (str): The text to print.
        color (str): The color to print the text in. Supported colors: 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta'.
    """
    colours = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'yellow': '\033[93m',
        'cyan': '\033[96m',
        'magenta': '\033[95m',
        'reset': '\033[0m'
    }
    
    if color in colours:
        print(f"{colours[color]}{text}{colours['reset']}")
    else:
        print("Unsupported color. Available colors: red, green, blue, yellow, cyan, magenta.")

def print_centered(text, width=80):
    """
    Prints text centered within a specified width.
    
    Args:
        text (str): The text to print.
        width (int): The width to center the text within.
    """
    print(text.center(width))  # Center the text within the specified width

def print_menu(options, selected_index):
    for index, option in enumerate(options):
        if index == selected_index:
            print(f"> {print_bold(option)}")
        else:
            print(f"  {option}")