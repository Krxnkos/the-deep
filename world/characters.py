class Character:
    def __init__(self, name, description, backstory, health=100):
        self.name = name
        self.description = description
        self.backstory = backstory
        self.health = health
        self.inventory = []

    def interact(self):
        return f"You interact with {self.name}. {self.description}"

    def add_item(self, item):
        self.inventory.append(item)
        return f"{item} has been added to {self.name}'s inventory."

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return f"{item} has been removed from {self.name}'s inventory."
        return f"{self.name} does not have {item} in their inventory."

    def show_inventory(self):
        if self.inventory:
            return f"{self.name}'s Inventory: " + ", ".join(self.inventory)
        return f"{self.name} has no items in their inventory."

# Define the characters in the game
dr_mira_elson = Character(
    name="Dr. Mira Elson",
    description="A marine biologist and former researcher at Erebus-9.",
    backstory="Left frantic notes warning about 'The Awakening' beneath the trench."
)

captain_theo_nash = Character(
    name="Captain Theo Nash",
    description="A submarine pilot and war veteran with PTSD.",
    backstory="Your guide through the trench—until he begins to hear voices."
)

echo = Character(
    name="Echo",
    description="An AI originally designed to assist with oceanic data collection.",
    backstory="Now glitching—sometimes helpful, sometimes cryptic or malicious."
)

tidecaller = Character(
    name="The Tidecaller",
    description="A mythic, shapeless entity representing the ocean's wrath.",
    backstory="Speaks through dreams and madness."
)