def load_ascii_art(file_path):
    """Load ASCII art from a specified file."""
    try:
        with open(file_path, 'r') as file:
            art = file.read()
        return art
    except FileNotFoundError:
        return "ASCII art not found."

def display_title():
    """Display the game title ASCII art."""
    title_art = load_ascii_art('resources/ascii/title.txt')
    print(title_art)

def display_location_art(location):
    """Display ASCII art for a specific location."""
    location_art_map = {
        'erebus9': 'resources/ascii/locations/erebus9.txt',
        'trench': 'resources/ascii/locations/trench.txt',
        'ghost_reef': 'resources/ascii/locations/ghost_reef.txt',
        'fishing_trawler': 'resources/ascii/locations/fishing_trawler.txt',
        'black_bloom': 'resources/ascii/locations/black_bloom.txt'
    }
    art = load_ascii_art(location_art_map.get(location, ''))
    print(art)

def display_item_art(item):
    """Display ASCII art for a specific item."""
    item_art_map = {
        'scanner': 'resources/ascii/items/scanner.txt',
        'journal': 'resources/ascii/items/journal.txt',
        'coral': 'resources/ascii/items/coral.txt',
        'talisman': 'resources/ascii/items/talisman.txt',
        'flare_gun': 'resources/ascii/items/flare_gun.txt'
    }
    art = load_ascii_art(item_art_map.get(item, ''))
    print(art)