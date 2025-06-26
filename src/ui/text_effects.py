import sys
import time
import os
import tkinter as tk
from threading import Thread

def print_typing_effect(text, delay=0.05):
    """
    Prints text with a typing effect.
    
    Args:
        text (str): The text to print.
        delay (float): The delay between each character.
    """
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

def typewriter_effect(text, delay=0.5):  # Increased from 0.03 to 0.08 for slower effect
    """
    Display text with a typewriter effect.
    
    Args:
        text (str): The text to display
        delay (float): Delay between characters in seconds
    """
    # Process text to handle potential formatting issues
    lines = text.split("\n")
    processed_lines = []
    
    # Clean up indentation to prevent formatting issues
    for line in lines:
        if line.strip():  # Skip empty lines
            processed_lines.append(line.lstrip())
    
    # Join back into a single string
    processed_text = "\n".join(processed_lines)
    
    # Print the text character by character
    for char in processed_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    
    # Ensure a newline at the end
    if not processed_text.endswith("\n"):
        print()

def fade_in_text(text, steps=10, delay=0.05):
    """
    Display text with a fade-in effect using console brightness.
    
    Args:
        text (str): The text to display
        steps (int): Number of brightness steps
        delay (float): Delay between steps in seconds
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Create brightness levels using characters of increasing "weight"
    brightness_levels = [
        ' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'
    ]
    
    for level in range(steps):
        os.system('cls' if os.name == 'nt' else 'clear')
        brightness_char = brightness_levels[min(level, len(brightness_levels)-1)]
        for line in text.split('\n'):
            print(line.replace('@', brightness_char))
        time.sleep(delay)
    
    # Final display with actual text
    os.system('cls' if os.name == 'nt' else 'clear')
    print(text)

def horror_text_effect(text, flicker_count=3, delay=0.1):
    """
    Display text with a horror-themed flickering effect.
    
    Args:
        text (str): The text to display
        flicker_count (int): Number of flickers
        delay (float): Delay between flickers in seconds
    """
    
    # Display the text with flickering effect
    for i in range(flicker_count):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(text)
        time.sleep(delay)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(delay / 2)
    
    # Final display
    print(text)

class TypewriterEffect:
    def __init__(self, text_widget, text, base_delay=0.3):
        """
        Initialize typewriter effect for GUI
        
        Args:
            text_widget: tkinter Text or Label widget
            text (str): The text to display
            base_delay (float): Base delay between characters in seconds
        """
        self.text_widget = text_widget
        self.text = text
        self.base_delay = base_delay * 1000  # Convert to milliseconds
        self.char_index = 0
        self.is_running = False
        self.pause_after_punctuation = {
            '.': 2000,  # 2000ms (2 sec) pause after periods
            '!': 2000,  # 2000ms pause after exclamation marks
            '?': 2000,  # 2000ms pause after question marks
            ',': 1000,  # 1000ms (1 sec) pause after commas
            '\n': 1500, # 1500ms pause after new lines
            ' ': 300,   # 300ms pause after spaces
        }
    
    def start(self):
        """Start the typewriter effect"""
        self.char_index = 0
        self.is_running = True
        self._type_text()
    
    def stop(self):
        """Stop the typewriter effect"""
        self.is_running = False
    
    def _type_text(self):
        """Type text character by character with dynamic delays"""
        if not self.is_running:
            return
            
        if self.char_index < len(self.text):
            # Update the text
            current_text = self.text[:self.char_index + 1]
            self.text_widget.config(text=current_text)
            
            # Calculate delay for next character
            current_char = self.text[self.char_index]
            
            # Base delay plus any additional pause for punctuation
            next_delay = self.base_delay
            if current_char in self.pause_after_punctuation:
                next_delay += self.pause_after_punctuation[current_char]
            
            self.char_index += 1
            
            # Schedule next character with proper delay
            self.text_widget.after(int(next_delay), self._type_text)

def show_text_with_effect(text):
    """
    Display text with typewriter effect in a GUI window
    
    Args:
        text (str): The text to display
    """
    root = tk.Tk()
    root.title("The Deep")
    root.geometry("600x400")
    
    # Configure the label with proper styling
    label = tk.Label(
        root,
        text="",
        wraplength=500,
        justify=tk.LEFT,
        font=("Courier", 14),
        bg="black",
        fg="green"
    )
    label.pack(padx=40, pady=40, expand=True, fill='both')
    
    # Create effect with much slower base delay
    effect = TypewriterEffect(label, text, base_delay=0.3)  # 300ms between characters
    effect.start()
    
    # Keep window running
    root.mainloop()