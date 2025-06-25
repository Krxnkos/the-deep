"""
GUI menu utilities for The Deep game.
"""

import tkinter as tk
import logging

logger = logging.getLogger('the_deep.gui_menu')

class GUIMenu:
    """GUI-based menu with arrow key navigation"""
    def __init__(self, gui, options):
        self.gui = gui
        self.options = options
        self.selected_index = 0
        
        # Update the GUI menu display
        self.gui.set_menu_options(options)
        logger.debug(f"Created GUI menu with {len(options)} options")
        
    def navigate(self, direction):
        """Navigate the menu options"""
        if direction == "up":
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif direction == "down":
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        # Update the GUI to reflect the new selection
        self.gui.selected_option = self.selected_index
        self.gui.update_menu_selection()
        logger.debug(f"Menu navigation: {direction}, selected: {self.options[self.selected_index]}")
        
    def select(self):
        """Select the current option"""
        selected = self.options[self.selected_index]
        logger.debug(f"Menu selection: {selected}")
        return selected
