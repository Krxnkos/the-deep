class Location:
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
            print(f"ASCII art for {self.name} not found.")
        
    def describe(self):
        print(f"You are at: {self.name}")
        print(self.description)

# Define the locations
locations = {
    "Erebus-9": Location(
        name="Abandoned Deep-Sea Research Station 'Erebus-9'",
        description= (
            "Partially flooded and dimly powered, this research station holds "
            "logs hinting at strange discoveries and psychological breakdowns. "
            "Features tight corridors, flooded labs, and a bio-lab overrun with mutated coral."
        ),
        ascii_art_file="resources/ascii/locations/erebus9.txt"
    ),
    "Trench": Location(
        name="The Trench (Abyssal Rift)",
        description=(
            "A seemingly bottomless pit where players descend via submersible. "
            "Audio logs and eerie sightings escalate tension the deeper they go."
        ),
        ascii_art_file="resources/ascii/locations/trench.txt"
    ),
    "Ghost Reef": Location(
        name="Ghost Reef",
        description=(
            "A dead coral reef covered in plastic and sludge. "
            "Strange whispering can be heard underwater, and glowing bioluminescent "
            "growths hint at something unnatural feeding on waste."
        ),
        ascii_art_file="resources/ascii/locations/ghost_reef.txt"
    ),
    "Fishing Trawler": Location(
        name="Derelict Fishing Trawler",
        description=(
            "This vessel was illegally dumping chemical waste. Crew logs show "
            "progressive madness and hallucinations. The engine room may contain a "
            "'living' nest of something grotesque."
        ),
        ascii_art_file="resources/ascii/locations/fishing_trawler.txt"
    ),
    "Black Bloom": Location(
        name="The Black Bloom",
        description=(
            "A mysterious underwater forest of oil-slick black kelp. Some tendrils "
            "seem to move on their own, and the water here distorts sound and light."
        ),
        ascii_art_file="resources/ascii/locations/black_bloom.txt"
    )
}