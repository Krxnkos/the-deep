"""
Game engine for The Deep.
Handles main game logic and state.
"""

import sys
import os
import random
import time
import logging
from game.game_state import GameState

# Fix the import path for the Player class
try:
    from player.player import Player
except ModuleNotFoundError:
    # Try alternative import paths
    try:
        from game.player import Player
    except ModuleNotFoundError:
        # If both fail, create a minimal Player class for now
        class Player:
            def __init__(self, name):
                self.name = name
                self.health = 100
                self.max_health = 100
                self.inventory = []
                self.journal = []
                self.samples = []

from world.enemies import get_random_enemy_for_location
from world.items import get_item_by_id
from ui.text_effects import typewriter_effect

# Setup logger
logger = logging.getLogger('the_deep.engine')

# ANSI color and style codes
class Colors:
    # ANSI color codes
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class GameEngine:
    def __init__(self, player=None):
        # Initialize without terminal-specific code
        self.player = player or Player("Explorer")
        self.game_state = GameState()
        self.current_location = self.game_state.current_location
        
        # Combat related settings
        self.current_enemy = None
        self.min_steps_between_combat = 3
        self.steps_since_combat = 0
        
        # Game state flags
        self.game_running = True
        
        # Game objectives initialization 
        self.game_objectives = {
            "collect_samples": {
                "name": "Collect Environmental Samples",
                "description": "Collect water, tissue and pollution samples from different locations to analyze the environmental impact.",
                "target": 5,
                "progress": 0,
                "completed": False
            },
            "document_mutations": {
                "name": "Document Mutations",
                "description": "Document evidence of how pollution has affected marine life through mutations.",
                "target": 3,
                "progress": 0,
                "completed": False
            },
            "map_pollution": {
                "name": "Map Pollution Sources",
                "description": "Identify and map the sources of pollution in the area.",
                "target": 3,
                "progress": 0,
                "completed": False
            },
            "find_research": {
                "name": "Recover Research Data",
                "description": "Find Dr. Mira Elson's research data on 'The Awakening'.",
                "target": 1,
                "progress": 0,
                "completed": False
            }
        }
        self.main_objective = {
            "name": "Stop the Tide",
            "description": "Discover the connection between the pollution and the Tidecaller entity, and find a way to prevent an ecological disaster.",
            "completed": False
        }
        self.educational_facts = self.load_educational_facts()
    
    def display_status_bar(self):
        """Display status bar with game and player information"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Get terminal width
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80  # Default if we can't detect terminal size
        
        # Format status information with color and health bar
        title = f"{Colors.CYAN}{Colors.BOLD}THE DEEP{Colors.RESET}"
        
        # Create health bar visualization
        health_percent = self.player.health / 100
        bar_length = 20
        filled_length = int(bar_length * health_percent)
        health_bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Color the health bar based on health percentage
        if health_percent > 0.7:
            health_color = Colors.GREEN
        elif health_percent > 0.3:
            health_color = Colors.YELLOW
        else:
            health_color = Colors.RED
    
        player_info = f"Player: {self.player.name} | Health: {health_color}{health_bar}{Colors.RESET} {self.player.health}/100"
        
        # Add location if available
        location_info = ""
        if self.current_location:
            location_info = f" | Location: {Colors.BOLD}{self.current_location.name}{Colors.RESET}"
        
        # Create status bar
        status_text = f"{title} - {player_info}{location_info}"
        
        # Print status bar with borders
        print(f"{Colors.BOLD}" + "=" * width + f"{Colors.RESET}")
        print(status_text)
        print(f"{Colors.BOLD}" + "=" * width + f"{Colors.RESET}")
        print()  # Empty line after status bar
    
    def start(self):
        """Start the game engine and begin the game."""
        self.game_running = True
        
        # Display introduction with status bar
        self.display_status_bar()
        self.display_intro()
        
        # Display educational mission briefing
        self.display_status_bar()
        self.display_mission_briefing()
        
        # Main game loop
        while self.game_running:
            # Always show status bar at the beginning of each loop
            self.display_status_bar()
            
            if self.current_enemy and self.current_enemy.is_alive():
                self.handle_combat()
            else:
                self.current_enemy = None
                self.process_current_location()
                
                # Random chance to spawn enemy (but not too often)
                if self.steps_since_combat >= self.min_steps_between_combat:
                    spawn_chance = 0.25  # 25% chance
                    if random.random() < spawn_chance:
                        self.spawn_enemy()
                        self.steps_since_combat = 0
            
                self.handle_player_input()
                self.steps_since_combat += 1
            
            # Check game over conditions
            if self.player.health <= 0:
                self.game_over("You have succumbed to the depths...")
                break
                
            # Check win condition
            if self.check_win_condition():
                self.win_game()
                break

    def _give_starter_items(self):
        """Give starter items to the player."""
        from world.items import get_item_by_id
        
        # Basic equipment
        flashlight = get_item_by_id("flashlight")
        if flashlight:
            self.player.add_to_inventory(flashlight)
        
        scanner = get_item_by_id("scanner")
        if scanner:
            self.player.add_to_inventory(scanner)
        
        medkit = get_item_by_id("medkit")
        if medkit:
            self.player.add_to_inventory(medkit)
        
        knife = get_item_by_id("dive_knife")
        if knife:
            self.player.add_to_inventory(knife)
    
    def load_educational_facts(self):
        """Load educational facts about marine pollution and ocean conservation."""
        return [
            "Ocean pollution affects over 700 marine species. An estimated 100 million marine animals die each year from plastic waste alone.",
            "Microplastics have been found in 100% of marine turtle species, 59% of whale species, 36% of seal species and 40% of seabird species examined.",
            "Only 9% of all plastic ever produced has been recycled. About 12% has been incinerated, while the rest ends up in landfills, dumps, or the natural environment.",
            "Over 80% of marine pollution comes from land-based activities. This includes oil, fertilizers, sewage, and industrial waste.",
            "The Great Pacific Garbage Patch is the largest accumulation of ocean plastic in the world and is located between Hawaii and California. It covers an estimated surface area of 1.6 million square kilometers.",
            "Deep sea ecosystems are particularly vulnerable to pollution as cold temperatures and limited light slow degradation processes. Pollutants can remain active in deep waters for centuries.",
            "Sound pollution from ships, sonar, and offshore drilling can travel for hundreds of miles underwater, disrupting the communication and navigation of marine animals like whales and dolphins.",
            "Chemical runoff from agriculture creates 'dead zones' in coastal areas where oxygen levels are so low that marine life cannot survive. There are now over 400 such zones worldwide.",
            "Coral reefs, which support 25% of all marine species, could disappear by 2050 due to pollution, climate change, and ocean acidification."
        ]
    
    def display_intro(self):
        """Display the game introduction sequence."""
        from ui.ascii_art import display_title
        
        display_title()
        intro_text = """
WELCOME TO THE DEEP

Beneath the surface lies more than darkness.

You are about to embark on a perilous journey to uncover 
the mysteries of the abandoned deep-sea research station Erebus-9.

Steel your nerves. Not everything you see or hear can be trusted.
"""
        typewriter_effect(intro_text)
        input("\nPress ENTER to begin your descent...")
    
    def display_mission_briefing(self):
        """Display the mission briefing with educational content"""
        briefing = """
MISSION BRIEFING
===============

Marine biologist Dr. Mira Elson disappeared while investigating alarming changes in deep sea ecosystems.
Her last transmissions mentioned "The Awakening" - a phenomenon possibly connected to increasing 
pollution levels in this region.

Your objectives:

1. Collect environmental samples to document pollution impact
2. Document mutations in marine life caused by chemical waste
3. Map sources of pollution in the area
4. Recover Dr. Elson's research data

MAIN OBJECTIVE: Determine the connection between pollution and the mysterious "Tidecaller" entity
that locals believe is awakening due to our abuse of the oceans.

EDUCATIONAL NOTE:
"""
        
        # Add a random educational fact
        fact = random.choice(self.educational_facts)
        briefing += fact
        
        typewriter_effect(briefing)
        
        print("\nCOMMAND HELP:")
        print("- Type 'north', 'south', 'east', 'west', 'up', or 'down' to move")
        print("- Type 'look' to examine your surroundings")
        print("- Type 'inventory' or 'i' to check your items")
        print("- Type 'help' for more commands")
        
        input("\nPress ENTER to begin your mission...")
    
    def process_current_location(self):
        """Process the current location and display relevant information."""
        if not self.current_location:
            # Set initial location if none exists
            from world.locations import get_starting_location
            self.current_location = get_starting_location()
            self.player.set_location(self.current_location.id)
    
        # Check if this is the first visit to show detailed description
        first_visit = not self.current_location.visited
        self.current_location.visited = True
        
        # Display location information
        print(f"\n{Colors.BOLD}=== {self.current_location.name} ==={Colors.RESET}")
        
        if first_visit:
            print(f"{Colors.CYAN}{self.current_location.description}{Colors.RESET}")
            
            # Educational content on first visit
            if "reef" in self.current_location.id:
                print(f"\n{Colors.YELLOW}EDUCATIONAL NOTE:{Colors.RESET} Coral reefs are among the most diverse ecosystems on Earth, but pollution, climate change, and ocean acidification have led to a 50% decline in coral reefs worldwide in the past 30 years.")
            elif "trench" in self.current_location.id:
                print(f"\n{Colors.YELLOW}EDUCATIONAL NOTE:{Colors.RESET} The deep ocean remains one of the least explored regions on Earth. Deep sea trenches can reach depths exceeding 36,000 feet, where pressure is more than 1,000 times that at sea level.")
            elif "bloom" in self.current_location.id:
                print(f"\n{Colors.YELLOW}EDUCATIONAL NOTE:{Colors.RESET} Algal blooms can create hypoxic conditions (low oxygen) that lead to 'dead zones' where marine life cannot survive. The largest dead zone in the world is in the Baltic Sea.")
            
            # Add journal entry for first visit
            self.player.add_journal_entry(f"Visited {self.current_location.name}. {self.current_location.description[:100]}...")
        else:
            # Shorter description for return visits
            print(f"You are back at {self.current_location.name}.")
            
        # Display any items in the location
        if self.current_location.items:
            print("\n{Colors.GREEN}You notice:{Colors.RESET}")
            for item in self.current_location.items:
                print(f"- {item.name}")
    
        # Always display available exits
        if self.current_location.exits:
            print("\n{Colors.CYAN}Possible directions:{Colors.RESET}")
            for direction, location_id in self.current_location.exits.items():
                print(f"- {direction}")

    def handle_combat(self):
        """Handle the combat encounter with the current enemy."""
        from world.enemies import Enemy
        
        enemy = self.current_enemy
        player = self.player
        
        print(f"\n{Colors.RED}{Colors.BOLD}WARNING: HOSTILE ENTITY DETECTED!{Colors.RESET}")
        print(f"Encountered: {enemy.name}")
        print(f"Your health: {player.health}/100 | {enemy.name}'s health: {enemy.health}/{enemy.max_health}")
        
        # Combat loop
        while enemy.is_alive() and player.health > 0:
            action = input("\nChoose an action: (attack, flee, use item) > ").lower().strip()
            
            if action == "attack":
                # Simple attack mechanism
                damage_dealt = random.randint(5, 15)
                damage_received = random.randint(5, 10)
                
                print(f"You attack the {enemy.name} for {damage_dealt} damage.")
                enemy.health -= damage_dealt
                
                # Show updated enemy health
                print(f"{enemy.name}'s health: {enemy.health}/{enemy.max_health}")
                
                if enemy.is_alive():
                    print(f"The {enemy.name} attacks you for {damage_received} damage.")
                    player.health -= damage_received
                    # Show updated player health
                    print(f"Your health: {player.health}/100")
                else:
                    # Clear win message
                    print(f"\n{Colors.GREEN}You have defeated the {enemy.name}!{Colors.RESET}")
                    # Handle rewards and item drops
                    self.handle_enemy_defeat(enemy)
                    self.current_enemy = None
                    break
                
            elif action == "flee":
                # Fleeing mechanism (simple success/failure)
                if random.random() < 0.5:
                    print(f"{Colors.YELLOW}You successfully fled from the encounter.{Colors.RESET}")
                    self.current_enemy = None
                    break
                else:
                    print(f"{Colors.RED}Failed to flee!{Colors.RESET}")
                    damage_received = random.randint(5, 10)
                    print(f"The {enemy.name} attacks you for {damage_received} damage.")
                    player.health -= damage_received
                    # Show updated player health
                    print(f"Your health: {player.health}/100")
                
            elif action == "use item":
                # Get a list of usable items
                usable_items = [item for item in player.inventory if hasattr(item, 'use')]
                
                if usable_items:
                    print("\nAvailable items:")
                    for idx, item in enumerate(usable_items, 1):
                        print(f"{idx}. {item.name}")
                    
                    try:
                        choice = int(input("\nChoose an item number (0 to cancel): "))
                        if choice == 0:
                            print("Cancelled item use.")
                            continue
                        
                        if 1 <= choice <= len(usable_items):
                            item = usable_items[choice-1]
                            result = item.use(player, self.current_location)
                            print(result)
                            # Show updated player health after using an item
                            print(f"Your health: {player.health}/100")
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print("You have no usable items.")
                
                # Enemy still gets to attack if you use an item
                if enemy.is_alive():
                    damage_received = random.randint(5, 10)
                    print(f"The {enemy.name} attacks you for {damage_received} damage.")
                    player.health -= damage_received
                    # Show updated player health
                    print(f"Your health: {player.health}/100")
            else:
                print("Invalid action. Choose again.")
    
    def spawn_enemy(self):
        """Spawn a random enemy at the current location."""
        enemy = get_random_enemy_for_location(self.current_location.id)
        
        if enemy:
            self.current_enemy = enemy
            enemy.health = enemy.max_health  # Reset enemy health
            print(f"A wild {enemy.name} appears!")
        else:
            print("No enemy found to spawn.")
    
    def move_player(self, direction):
        """Move player in the specified direction"""
        if not hasattr(self.current_location, 'exits') or direction not in self.current_location.exits:
            print(f"You can't go {direction} from here.")
            return False
            
        # Get the target location ID
        target_location_id = self.current_location.exits[direction]
        
        # Move to the new location - handle different GameState implementations
        if hasattr(self.game_state, 'get_location'):
            # Use the get_location method if available
            new_location = self.game_state.get_location(target_location_id)
            if new_location:
                self.current_location = new_location
            else:
                print(f"Error: Location '{target_location_id}' not found.")
                return False
        elif hasattr(self.game_state, 'locations') and target_location_id in self.game_state.locations:
            # Direct dictionary access if get_location is not available
            self.current_location = self.game_state.locations[target_location_id]
        else:
            print(f"Error: Cannot find location '{target_location_id}'.")
            return False
    
        # Update player's location if the method exists
        if hasattr(self.player, 'set_location'):
            self.player.set_location(self.current_location)
        
        # Display the new location
        self.process_current_location()
        return True
    
    def handle_player_input(self):
        """Get and process player input"""
        action = input("\nWhat would you like to do? > ").lower().strip()
    
        # Handle movement
        if action in ["north", "south", "east", "west", "up", "down"]:
            self.move_player(action)
        # Handle inventory
        elif action == "inventory" or action == "i":
            inventory_text = self.player.show_inventory()
            print(inventory_text)
        # Handle look command
        elif action == "look":
            print(self.current_location.description)
            if self.current_location.items:
                print("\nYou notice:")
                for item in self.current_location.items:
                    print(f"- {item.name}")
        # Handle journal
        elif action == "journal" or action == "j":
            journal_text = self.player.read_journal()
            print(journal_text)
        # Handle samples
        elif action == "samples" or action == "s":
            samples_text = self.player.view_samples()
            print(samples_text)
        # Handle examination
        elif action.startswith("examine ") or action.startswith("look at "):
            item = action.replace("examine ", "").replace("look at ", "")
            self.examine_item(item)
        # Handle taking items
        elif action.startswith("take ") or action.startswith("get "):
            item_name = action.replace("take ", "").replace("get ", "")
            self.take_item(item_name)
        # Handle using items
        elif action.startswith("use "):
            item_name = action.replace("use ", "")
            self.use_item(item_name)
        # Handle objectives view
        elif action == "objectives" or action == "o":
            self.show_objectives()
        # Handle help
        elif action == "help":
            self.show_help()
        # Handle quit
        elif action == "quit":
            if input("Are you sure you want to quit? (y/n) ").lower() == "y":
                self.game_running = False
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")

    def examine_item(self, item_name):
        """Examine an item in detail."""
        from world.items import get_item_by_id
        
        item = get_item_by_id(item_name)
        if item:
            print(f"Examining {item.name}: {item.description}")
        else:
            print("Item not found.")
    
    def take_item(self, item_name):
        """Take an item from the current location."""
        if not self.current_location or not self.current_location.items:
            print("There's nothing here to take.")
            return
        
        # Find the item in the location that matches the name
        for item in self.current_location.items[:]:  # Create a copy to avoid modification issues
            if item_name.lower() in item.name.lower():
                self.current_location.items.remove(item)
                self.player.add_to_inventory(item)
                print(f"{Colors.GREEN}You've taken the {item.name}.{Colors.RESET}")
                
                # Update relevant objectives
                if "sample" in item.id:
                    self.update_objective("collect_samples", 1)
                    print(f"{Colors.YELLOW}Sample added to your collection.{Colors.RESET}")
                elif "research" in item.id:
                    self.update_objective("find_research", 1)
                    print(f"{Colors.YELLOW}Research data recovered.{Colors.RESET}")
                
                return
        
        print(f"You don't see a {item_name} here.")

    def use_item(self, item_name):
        """Use an item from the player's inventory."""
        # Find the item in inventory
        for item in self.player.inventory[:]:  # Create a copy to avoid modification issues
            if item_name.lower() in item.name.lower():
                if hasattr(item, 'use') and callable(item.use):
                    result = item.use(self.player, self.current_location)
                    print(result)
                    
                    # Show health update if applicable
                    if "health" in result.lower() or "heal" in result.lower():
                        print(f"Health: {self.player.health}/100")
                    
                    # Remove consumable items
                    if hasattr(item, 'consumable') and item.consumable:
                        self.player.inventory.remove(item)
                
                return
        print(f"You don't have a {item_name}.")
    
    def show_objectives(self):
        """Display the current game objectives."""
        print("\n=== OBJECTIVES ===")
        for key, obj in self.game_objectives.items():
            status = "✓" if obj["completed"] else " "
            print(f"[{status}] {obj['name']}: {obj['description']} (Progress: {obj['progress']}/{obj['target']})")
        
        print("===================")
        print(f"MAIN OBJECTIVE: {self.main_objective['name']} - {self.main_objective['description']}")
    
    def show_help(self):
        """Display the help information."""
        help_text = """
COMMAND HELP:
- Movement: north, south, east, west, up, down
- Look around: look
- Check inventory: inventory or i
- Read journal: journal or j
- View samples: samples or s
- Examine item: examine [item name] or look at [item name]
- Take item: take [item name] or get [item name]
- Use item: use [item name]
- View objectives: objectives or o
- Help: help
- Quit: quit

"""
        print(help_text)
    
    def game_over(self, reason):
        """Handle game over scenario."""
        self.game_running = False
        print(f"\n{Colors.RED}{Colors.BOLD}GAME OVER{Colors.RESET}")
        print(reason)
        
        # Optionally, display final stats or achievements
        self.display_final_stats()
    
    def win_game(self):
        """Handle winning the game."""
        self.game_running = False
        print(f"\n{Colors.GREEN}{Colors.BOLD}YOU WIN!{Colors.RESET}")
        print("Congratulations, you have completed your mission and saved the Erebus-9 station.")
        
        # Optionally, display final stats or achievements
        self.display_final_stats()
    
    def display_final_stats(self):
        """Display the final statistics or achievements."""
        print("\n=== FINAL STATS ===")
        print(f"Player: {self.player.name}")
        print(f"Health: {self.player.health}/100")
        print("Objectives:")
        
        for key, obj in self.game_objectives.items():
            status = "✓" if obj["completed"] else "✗"
            print(f"- {obj['name']}: {status}")
        
        print("===================")
        print("Thank you for playing!")
        input("Press ENTER to exit...")
    
    def check_win_condition(self):
        """Check if all objectives are completed to trigger win condition"""
        all_objectives_complete = all(obj["completed"] for obj in self.game_objectives.values())
        
        # Final location requirement - player must be at the Black Bloom for final confrontation
        at_final_location = self.current_location and self.current_location.id == "black_bloom"
        
        # Need the special item to win - but make it easier to find
        has_special_item = any(item.id == "tidecaller_essence" for item in self.player.inventory)
        
        # If all other conditions are met but player doesn't have the item,
        # place it in the current location if they're at the final location
        if all_objectives_complete and at_final_location and not has_special_item:
            from world.items import get_item_by_id
            special_item = get_item_by_id("tidecaller_essence")
            if special_item and special_item not in self.current_location.items:
                self.current_location.add_item(special_item)
                print("\nThe water around you begins to shimmer with an otherworldly glow...")
                print("Something has formed in the center of the Black Bloom.")
        
        return all_objectives_complete and at_final_location and has_special_item
    
    def handle_enemy_defeat(self, enemy):
        """Handle enemy defeat rewards and educational content"""
        # Award some health for winning
        health_gain = random.randint(5, 15)
        self.player.health = min(100, self.player.health + health_gain)
        print(f"{Colors.GREEN}You recovered {health_gain} health points from the victory!{Colors.RESET}")
        print(f"Current health: {self.player.health}/100")
        
        # Educational content based on enemy type
        if "mutated" in enemy.id:
            self.update_objective("document_mutations", 1)
            print(f"\n{Colors.CYAN}EDUCATIONAL NOTE:{Colors.RESET}")
            print("You've documented evidence of genetic mutations caused by chemical pollution.")
            print("Marine life exposed to toxic chemicals can develop deformities and behavioral changes.")
            
            # Add journal entry
            self.player.add_journal_entry(f"Encountered {enemy.name}. The mutations appear to be caused by chemical waste exposure.")
            
        elif "plastic" in enemy.id:
            self.update_objective("map_pollution", 1)
            print(f"\n{Colors.CYAN}EDUCATIONAL NOTE:{Colors.RESET}")
            print("Plastic waste takes hundreds of years to decompose in marine environments.")
            print("Many animals mistake plastic fragments for food, leading to starvation and death.")
            
        # Check for item drops
        loot_chance = random.random()
        if loot_chance < 0.7:  # 70% chance of getting loot
            # Create appropriate loot based on enemy type
            from world.items import get_item_by_id
            
            loot_options = []
            if "angler" in enemy.id:
                loot_options = ["fish_tissue", "water_sample"]
            elif "plastic" in enemy.id:
                loot_options = ["plastic_sample", "water_sample"]
            elif "chemical" in enemy.id:
                loot_options = ["chemical_sample"]
            elif "bloom" in enemy.id:
                loot_options = ["corrupted_tissue"]
                
            if loot_options:
                loot_id = random.choice(loot_options)
                loot_item = get_item_by_id(loot_id)
                
                if loot_item:
                    print(f"\n{Colors.YELLOW}The {enemy.name} dropped: {loot_item.name}{Colors.RESET}")
                    self.current_location.add_item(loot_item)
                    
                    # Update sample collection objective
                    if "sample" in loot_id or "tissue" in loot_id:
                        self.update_objective("collect_samples", 1)
    
        # Increase steps since combat
        self.steps_since_combat = 0
    
    def display_ascii_art(self, art_file):
        """Display ASCII art in the terminal"""
        # Check if we're in GUI mode
        if hasattr(self, '_prevent_terminal_mode') and self._prevent_terminal_mode:
            # Let the subclass handle it
            return
            
        # Terminal mode code
        from ui.ascii_art import load_ascii_art
        
        art = load_ascii_art(art_file)
        if art:
            print(art)
        else:
            logger.warning(f"Could not load ASCII art: {art_file}")
            
        # Terminal mode code
        from ui.ascii_art import load_ascii_art
        
        art = load_ascii_art(art_file)
        if art:
            print(art)
        else:
            logger.warning(f"Could not load ASCII art: {art_file}")
