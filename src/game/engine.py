import random
from ui.text_effects import typewriter_effect
from world.enemies import get_random_enemy_for_location

class GameEngine:
    def __init__(self, player=None):
        from game.player import Player
        self.player = player if player else Player("Explorer")
        self.game_running = False
        self.current_location = None
        self.current_enemy = None
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
        
    def load_educational_facts(self):
        """Load educational facts about marine pollution and ecology"""
        return [
            "Over 8 million tons of plastic waste enters our oceans every year.",
            "Approximately 80% of marine pollution comes from land-based activities.",
            "Deep sea creatures are particularly vulnerable to pollution due to the stable nature of their environment.",
            "Microplastics have been found in marine organisms living in the deepest parts of our oceans.",
            "Sound pollution from ships can disrupt communication between marine mammals like whales and dolphins.",
            "Chemical pollutants can cause mutations in marine life, affecting reproduction and survival rates.",
            "Coral reefs are dying worldwide due to ocean acidification, a direct result of increased CO2 in the atmosphere.",
            "Marine animals can mistake plastic waste for food, leading to starvation when their stomachs fill with indigestible materials.",
            "Oil spills can persist in deep ocean environments for decades due to slow decomposition rates in cold water.",
            "Dead zones are areas where oxygen levels are too low to support marine life, often caused by agricultural runoff."
        ]

    def start(self):
        """Start the game engine and begin the game."""
        self.game_running = True
        self.display_intro()
        
        # Display educational mission briefing
        self.display_mission_briefing()
        
        # Main game loop
        while self.game_running:
            if self.current_enemy and self.current_enemy.is_alive():
                self.handle_combat()
            else:
                self.current_enemy = None
                self.process_current_location()
                
                # Random chance to spawn an enemy
                if random.random() < 0.3 and not self.current_enemy:  # 30% chance
                    self.spawn_enemy()
                
                self.handle_player_input()
            
            # Check game over conditions
            if self.player.health <= 0:
                self.game_over("You have succumbed to the depths...")
                break
                
            # Check win condition
            if self.check_win_condition():
                self.win_game()
                break

    def display_intro(self):
        """Display the game introduction sequence."""
        from ui.ascii_art import display_title
        from ui.text_effects import typewriter_effect
        
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
        input("\nPress ENTER to begin your mission...")

    def process_current_location(self):
        """Process the current location and display relevant information."""
        if not self.current_location:
            # Set initial location if none exists
            from world.locations import get_starting_location
            self.current_location = get_starting_location()
            
        # Display location information
        print(f"\n=== {self.current_location.name} ===")
        print(self.current_location.description)
        
        # Display available exits
        if self.current_location.exits:
            print("\nPossible directions:")
            for direction, location_id in self.current_location.exits.items():
                print(f"- {direction}")
    
    def handle_player_input(self):
        """Process player input for the current game state."""
        action = input("\nWhat would you like to do? > ").lower().strip()
        
        # Handle movement
        if action in ["north", "south", "east", "west", "up", "down"]:
            self.move_player(action)
        # Handle inventory
        elif action == "inventory" or action == "i":
            print(self.player.show_inventory())
        # Handle examination
        elif action.startswith("examine ") or action.startswith("look at "):
            item = action.replace("examine ", "").replace("look at ", "")
            self.examine_item(item)
        # Handle help
        elif action == "help":
            self.show_help()
        # Handle quit
        elif action == "quit":
            if input("Are you sure you want to quit? (y/n) ").lower() == "y":
                self.game_running = False
        else:
            print("I don't understand that command.")
    
    def move_player(self, direction):
        """Move the player in the specified direction."""
        if direction in self.current_location.exits:
            from world.locations import get_location_by_id
            next_location_id = self.current_location.exits[direction]
            self.current_location = get_location_by_id(next_location_id)
            self.player.set_location(self.current_location.id)
        else:
            print(f"You can't go {direction} from here.")
    
    def examine_item(self, item_name):
        """Examine an item in the environment or inventory."""
        # Check if item is in the current location
        for item in self.current_location.items:
            if item.name.lower() == item_name:
                print(item.description)
                return
                
        # Check if item is in inventory
        for item in self.player.inventory:
            if item.name.lower() == item_name:
                print(item.description)
                return
                
        print(f"You don't see a {item_name} here.")
    
    def show_help(self):
        """Display help information for the player."""
        help_text = """
        AVAILABLE COMMANDS:
        - north, south, east, west, up, down: Move in a direction
        - inventory (or i): Check your inventory
        - examine [item]: Look closely at an item
        - take [item]: Pick up an item
        - use [item]: Use an item from your inventory
        - help: Display this help message
        - quit: Exit the game
        """
        print(help_text)
    
    def spawn_enemy(self):
        """Attempt to spawn an enemy appropriate for the current location"""
        if not self.current_location:
            return
            
        enemy = get_random_enemy_for_location(self.current_location.id)
        if enemy:
            self.current_enemy = enemy
            print(f"\nAlert! A {enemy.name} appears!")
            print(enemy.describe())

    def handle_combat(self):
        """Handle combat with the current enemy"""
        print(f"\n==== COMBAT: {self.current_enemy.name} ====")
        print("Options:")
        print("1. Attack with weapon")
        print("2. Try to escape")
        print("3. Use item")
        
        choice = input("> ")
        
        if choice == "1":
            # Check if player has a weapon
            weapons = [item for item in self.player.inventory if isinstance(item, self.get_weapon_class())]
            
            if not weapons:
                print("You don't have any weapons!")
                # Enemy still attacks
                damage, message = self.current_enemy.attack()
                print(message)
                self.player.take_damage(damage)
                print(f"Your health: {self.player.health}/100")
                return
            
            # Let player choose weapon if they have multiple
            weapon = weapons[0]
            if len(weapons) > 1:
                print("Choose a weapon:")
                for i, w in enumerate(weapons):
                    print(f"{i+1}. {w.name}")
                    
                weapon_choice = input("> ")
                try:
                    weapon_index = int(weapon_choice) - 1
                    if 0 <= weapon_index < len(weapons):
                        weapon = weapons[weapon_index]
                    else:
                        print("Invalid choice, using first weapon.")
                        weapon = weapons[0]
                except ValueError:
                    print("Invalid choice, using first weapon.")
                    weapon = weapons[0]
            
            # Player attacks
            damage, message = weapon.attack(self.current_enemy)
            print(message)
            
            # Enemy takes damage
            result = self.current_enemy.take_damage(damage)
            print(result)
            
            # Check if enemy is defeated
            if not self.current_enemy.is_alive():
                self.handle_enemy_defeat()
                return
                
            # Enemy attacks back
            damage, message = self.current_enemy.attack()
            print(message)
            self.player.take_damage(damage)
            print(f"Your health: {self.player.health}/100")
                
        elif choice == "2":
            # Try to escape
            if random.random() < 0.6:  # 60% escape chance
                print("You managed to escape!")
                self.current_enemy = None
            else:
                print("You couldn't escape!")
                # Enemy attacks
                damage, message = self.current_enemy.attack()
                print(message)
                self.player.take_damage(damage)
                print(f"Your health: {self.player.health}/100")
                
        elif choice == "3":
            # Display inventory for using items
            items = self.player.inventory
            if not items:
                print("You don't have any items to use!")
                return
                
            print("Choose an item to use:")
            for i, item in enumerate(items):
                print(f"{i+1}. {item.name}")
                
            try:
                item_choice = int(input("> ")) - 1
                if 0 <= item_choice < len(items):
                    item = items[item_choice]
                    if item.usable:
                        result = item.use(self.player, self.current_location)
                        print(result)
                    else:
                        print(f"You can't use the {item.name} in combat!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid choice.")
                
            # Enemy still attacks
            damage, message = self.current_enemy.attack()
            print(message)
            self.player.take_damage(damage)
            print(f"Your health: {self.player.health}/100")
        
        else:
            print("Invalid choice.")
            # Enemy still attacks
            damage, message = self.current_enemy.attack()
            print(message)
            self.player.take_damage(damage)
            print(f"Your health: {self.player.health}/100")

    def get_weapon_class(self):
        """Get the Weapon class for isinstance checks"""
        from world.items import Weapon
        return Weapon
        
    def handle_enemy_defeat(self):
        """Handle enemy defeat - loot, XP, educational content"""
        print(f"\nYou have defeated the {self.current_enemy.name}!")
        
        # Get loot
        loot_id = self.current_enemy.get_loot()
        if loot_id:
            from world.items import get_item_by_id
            loot_item = get_item_by_id(loot_id)
            if loot_item:
                print(f"You found: {loot_item.name}!")
                self.player.add_to_inventory(loot_item)
                
                # Update objectives if applicable
                if "tissue" in loot_id or "sample" in loot_id:
                    self.update_objective("collect_samples")
                if "tissue" in loot_id and "mutation" in self.current_enemy.description.lower():
                    self.update_objective("document_mutations")
        
        # Display educational content about the enemy
        if "plastic" in self.current_enemy.name.lower():
            fact = "Plastic pollution affects over 700 marine species. Animals get entangled in plastic waste or ingest it, often with fatal consequences."
        elif "chemical" in self.current_enemy.name.lower():
            fact = "Chemical pollutants like PCBs and heavy metals can accumulate in marine food chains, leading to biomagnification where top predators have the highest toxin levels."
        elif "bloom" in self.current_enemy.name.lower():
            fact = "Harmful algal blooms occur when pollution (often from agricultural runoff) causes explosive growth of algae, depleting oxygen and sometimes releasing toxins."
        else:
            fact = random.choice(self.educational_facts)
            
        print("\nEDUCATIONAL NOTE:")
        print(fact)
        
        # Reset enemy
        self.current_enemy = None
        input("\nPress ENTER to continue...")

    def update_objective(self, objective_key):
        """Update progress on an objective"""
        if objective_key in self.game_objectives:
            obj = self.game_objectives[objective_key]
            if not obj["completed"]:
                obj["progress"] += 1
                print(f"\nObjective update: {obj['name']} - {obj['progress']}/{obj['target']}")
                
                if obj["progress"] >= obj["target"]:
                    obj["completed"] = True
                    print(f"Objective COMPLETED: {obj['name']}!")

    def check_win_condition(self):
        """Check if all objectives are completed to trigger win condition"""
        all_objectives_complete = all(obj["completed"] for obj in self.game_objectives.values())
        
        # Final location requirement - player must be at the Black Bloom for final confrontation
        at_final_location = self.current_location and self.current_location.id == "black_bloom"
        
        # Need the special item to win
        has_special_item = any(item.id == "tidecaller_essence" for item in self.player.inventory)
        
        return all_objectives_complete and at_final_location and has_special_item

    def win_game(self):
        """Handle game win condition"""
        win_text = """
        As you stand among the eerie black tendrils of the Bloom, holding the glowing Tidecaller's 
        essence, you finally understand Dr. Elson's research.
        
        The Tidecaller isn't a monster - it's the ocean itself, responding to humanity's abuse. 
        The mutations, the strange phenomena - all are attempts by the marine ecosystem to adapt 
        to our pollution.
        
        Using Dr. Elson's data and your own samples, you've proven the connection between chemical 
        dumping and the awakening of this ancient defense mechanism.
        
        You release the essence back into the water with a silent promise: to share this knowledge, 
        to fight for better protections, to respect the deep.
        
        The tendrils around you shift, no longer threatening. You've been judged, and humanity 
        has been given another chance.
        
        EDUCATIONAL CONCLUSION:
        Our oceans sustain all life on Earth. The damage we cause through pollution, overfishing, 
        and climate change threatens not just marine ecosystems but our own survival. But like in 
        your journey, knowledge and action can turn the tide.
        
        YOU HAVE COMPLETED YOUR MISSION.
        """
        
        typewriter_effect(win_text)
        self.game_running = False
        print("\nTHANK YOU FOR PLAYING THE DEEP")