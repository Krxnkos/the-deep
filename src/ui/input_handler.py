"""
Input compatibility layer for The Deep game.
Allows the game to work with both terminal input and GUI input.
"""

import keyboard
import time
import threading
import logging
import tkinter as tk
from ui.gui_menu import GUIMenu

logger = logging.getLogger('the_deep.input')

class InputHandler:
    """Input handler that works with both terminal and GUI input"""
    
    def __init__(self, gui=None):
        self.gui = gui
        self.input_ready = False
        self.input_value = None
        self.is_gui_mode = gui is not None
        
    def get_input(self, prompt, options=None):
        """Get input from the user
        
        Args:
            prompt (str): The prompt to display
            options (list, optional): List of options to display
            
        Returns:
            str: The user's input
        """
        if not self.is_gui_mode:
            # Terminal mode - use standard input
            if options:
                print("\n" + prompt)
                for i, option in enumerate(options):
                    print(f"{i+1}. {option}")
                
                choice = input("Enter your choice (number): ")
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(options):
                        return options[index]
                    else:
                        print("Invalid choice. Please try again.")
                        return self.get_input(prompt, options)
                except ValueError:
                    print("Please enter a number.")
                    return self.get_input(prompt, options)
            else:
                return input(prompt)
        else:
            # GUI mode - use the GUI for input
            return self.gui.get_player_input(prompt, options)
    
    def wait_for_key(self, key="enter"):
        """Wait for a specific key to be pressed"""
        if not self.is_gui_mode:
            input("Press Enter to continue...")
        else:
            # Use a simple dialog in GUI mode
            dialog = tk.Toplevel(self.gui.root)
            dialog.title("Continue")
            
            frame = tk.Frame(dialog)
            frame.pack(pady=10, padx=10)
            
            label = tk.Label(frame, text="Press Enter to continue...")
            label.pack()
            
            def close_dialog(event=None):
                dialog.destroy()
            
            dialog.bind("<Return>", close_dialog)
            dialog.protocol("WM_DELETE_WINDOW", close_dialog)
            
            # Wait for dialog to close
            self.gui.root.wait_window(dialog)
