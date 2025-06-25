class Item:
    def __init__(self, name, description, ascii_art_file):
        self.name = name
        self.description = description
        self.ascii_art_file = ascii_art_file

    def display_ascii_art(self):
        try:
            with open(self.ascii_art_file, 'r') as file:
                art = file.read()
                print(art)
        except FileNotFoundError:
            print("ASCII art file not found.")

# Define items based on the brief
abyssal_scanner = Item(
    name="Abyssal Scanner",
    description="Detects movement or heat signatures through walls. May show things that shouldn’t be there.",
    ascii_art_file="resources/ascii/items/scanner.txt"
)

waterproof_journal = Item(
    name="Waterproof Journal",
    description="Collect clues, logs, and sketches from past researchers. Reveals character backstory and game lore.",
    ascii_art_file="resources/ascii/items/journal.txt"
)

corrupted_coral_sample = Item(
    name="Corrupted Coral Sample",
    description="Glows when near paranormal events. Starts to change shape the deeper you go.",
    ascii_art_file="resources/ascii/items/coral.txt"
)

divers_talisman = Item(
    name="Diver’s Talisman",
    description="Made from bone and sea glass. Said to protect from 'what sleeps in the tide.' May prevent or cause hallucinations depending on how it's used.",
    ascii_art_file="resources/ascii/items/talisman.txt"
)

emergency_flare_gun = Item(
    name="Emergency Flare Gun",
    description="Light source and weapon—but use it wisely, it draws attention. Has limited flares.",
    ascii_art_file="resources/ascii/items/flare_gun.txt"
)

# List of all items
items = [
    abyssal_scanner,
    waterproof_journal,
    corrupted_coral_sample,
    divers_talisman,
    emergency_flare_gun
]