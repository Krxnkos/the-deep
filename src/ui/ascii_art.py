"""
ASCII art loader for The Deep game.
"""

import os
import logging
from utils.config import Config

logger = logging.getLogger('the_deep.ui.ascii_art')

def display_title():
    """Display the game title in ASCII art."""
    title_art = """
    ████████╗██╗  ██╗███████╗    ██████╗ ███████╗███████╗██████╗ 
    ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔══██╗
       ██║   ███████║█████╗      ██║  ██║█████╗  █████╗  ██████╔╝
       ██║   ██╔══██║██╔══╝      ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ 
       ██║   ██║  ██║███████╗    ██████╔╝███████╗███████╗██║     
       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚══════╝╚═╝     
                                                                 
    ============================================================
     Beneath the surface lies more than darkness...
    ============================================================
    """
    print(title_art)

def load_ascii_art(art_file):
    """Load ASCII art from a file in the assets directory"""
    try:
        # Build paths correctly
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        art_path = os.path.join(script_dir, "ui", "assets", art_file)
        
        # Check if alternative location exists
        if not os.path.exists(art_path):
            alt_path = os.path.join(script_dir, "assets", art_file)
            if os.path.exists(alt_path):
                art_path = alt_path
                
        # Print paths for debugging
        logger.debug(f"Attempting to load ASCII art from: {art_path}")
        
        # If file exists, load and return it
        if os.path.exists(art_path):
            with open(art_path, 'r') as file:
                return file.read()
        else:
            logger.warning(f"ASCII art file not found: {art_path}")
            return None
            
    except Exception as e:
        logger.error(f"Error loading ASCII art: {str(e)}")
        return None

def display_location_art(location_name):
    """
    Display ASCII art for a location.
    
    Args:
        location_name (str): Name of the location
    """
    art = load_ascii_art(f"locations/{location_name.lower().replace(' ', '_')}.txt")
    if art:
        print(art)

def display_item_art(item_name):
    """
    Display ASCII art for an item.
    
    Args:
        item_name (str): Name of the item
    """
    art = load_ascii_art(f"items/{item_name.lower().replace(' ', '_')}.txt")
    if art:
        print(art)