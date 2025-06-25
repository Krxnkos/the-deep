import os
from utils.config import Config

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

def load_ascii_art(filename):
    """
    Load ASCII art from a file.
    
    Args:
        filename (str): Name of the ASCII art file
        
    Returns:
        str: The ASCII art content or None if file not found
    """
    try:
        file_path = os.path.join(Config.ASSETS_PATH, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"ASCII art not found: {filename}")
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