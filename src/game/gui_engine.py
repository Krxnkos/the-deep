"""
GUI version of the game engine.
Uses tkinter for display and keyboard for input.
"""

import random
import os
import sys
import threading
import time
import logging
from world.enemies import get_random_enemy_for_location
from world.items import get_item_by_id
from game.engine import GameEngine, Colors
from game.game_state import GameState  # Import GameState explicitly
from ui.ascii_art import display_title

# Setup logger
logger = logging.getLogger('the_deep.gui_engine')

class GUIGameEngine(GameEngine):
    def __init__(self, player=None):
        # Set this flag before calling super().__init__
        self._prevent_terminal_mode = True
        
        # Initialize with just the player parameter
        super().__init__(player)
        
        # Override any terminal-specific initializations
        self.game_state = None  # We'll initialize this in the start method
        
        # Ensure Tkinter is properly imported
        try:
            import tkinter as tk
            self.root = tk.Tk()
            self.root.title("THE DEEP - Ocean Exploration Game")
            self.root.geometry("800x600")  # Set window size
            self.root.withdraw()  # Hide window initially
            
            # Create GUI
            from ui.gui import GameGUI
            self.gui = GameGUI(self.root)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            
            logger.info("Successfully created GUI window")
        except Exception as e:
            logger.error(f"Failed to create GUI: {str(e)}")
            print(f"\nError: Could not create GUI window. {str(e)}")
            raise
        
        # Input/output flags
        self.input_ready = False
        self.input_value = None
        self.current_options = []
        self.selecting_menu_option = False
        self.running = True
        self.enter_keys_used = 0  # Track enter key usage
        
    def on_close(self):
        """Handle window close event"""
        self.running = False
        self.game_running = False
        self.root.destroy()
        sys.exit(0)
        
    def start(self):
        """Start the game in the GUI window"""
        try:
            # Initialize game state here to prevent terminal mode initialization
            self.game_state = GameState()
            self.current_location = self.game_state.current_location
            self.game_running = True
            
            # Show the window now that it's ready
            self.root.deiconify()
            self.root.update()
            
            # Start game logic in a separate thread
            self.game_thread = threading.Thread(target=self.game_loop)
            self.game_thread.daemon = True
            self.game_thread.start()
            
            # Start the tkinter main loop
            logger.info("Starting GUI main loop")
            self.gui.run()
        except Exception as e:
            logger.error(f"Error starting GUI game: {str(e)}")
            print(f"\nError starting GUI game: {str(e)}")
            raise
        
    def get_available_actions(self):
        """Get available actions based on current location."""
        try:
            actions = []
            
            # Check if current_location exists
            if not hasattr(self, 'current_location') or not self.current_location:
                logger.error("Current location not properly initialized")
                return ["Look around", "Inventory", "Help", "Quit"]
                
            # Handle different location attributes
            if hasattr(self.current_location, 'exits') and self.current_location.exits:
                for direction, location_id in self.current_location.exits.items():
                    actions.append(f"Move ({direction})")
            
            # Add standard actions
            actions.append("Look around")
            actions.append("Inventory")
            actions.append("Journal")
            actions.append("Samples")
            actions.append("Objectives")
            
            # Add item-specific actions if location has items
            if hasattr(self.current_location, 'items') and self.current_location.items:
                for item in self.current_location.items:
                    actions.append(f"Examine {item.name}")
                    actions.append(f"Take {item.name}")
                    
            # Add inventory item actions
            if self.player and self.player.inventory:
                for item in self.player.inventory:
                    # For weapons, show equip/unequip status
                    if hasattr(item, 'equipped') and item.equipped:
                        actions.append(f"Use {item.name} (Unequip)")
                    else:
                        actions.append(f"Use {item.name}")
            
            actions.append("Help")
            actions.append("Quit")
            
            return actions
        except Exception as e:
            logger.error(f"Error in get_available_actions: {str(e)}")
            # Return a safe default set of actions
            return ["Look around", "Help", "Quit"]

    def game_loop(self):
        """Main game logic loop, runs in a separate thread"""
        logger.info("Starting game logic thread")
        
        try:
            # Display introduction with status bar
            self.display_status_bar()
            self.display_intro()
            
            # Display educational mission briefing
            self.display_status_bar()
            self.display_mission_briefing()
            
            # Main game loop
            while self.game_running and self.running:
                try:
                    # Always show status bar at the beginning of each loop
                    self.display_status_bar()
                    
                    if self.current_enemy and self.current_enemy.is_alive():
                        self.handle_combat()
                    else:
                        self.current_enemy = None
                        self.process_current_location()
                        
                        # Random chance to spawn enemy (but not too often)
                        if hasattr(self, 'steps_since_combat') and self.steps_since_combat >= self.min_steps_between_combat:
                            spawn_chance = 0.25  # 25% chance
                            if random.random() < spawn_chance:
                                self.spawn_enemy()
                                self.steps_since_combat = 0
                
                        self.handle_player_input()
                        
                        # Increment steps counter if it exists
                        if hasattr(self, 'steps_since_combat'):
                            self.steps_since_combat += 1
                        else:
                            self.steps_since_combat = 0
                
                    # Check game over conditions
                    if self.player.health <= 0:
                        self.game_over("You have succumbed to the depths...")
                        break  # Exit the loop when game is over
                        
                    # Add a delay to prevent CPU hogging and allow UI updates
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error in game loop iteration: {str(e)}")
                    self.display_text(f"An error occurred: {str(e)}\nPlease report this bug.")
                    time.sleep(2)
                    # Don't break the loop on errors, try to continue
        except Exception as e:
            logger.error(f"Fatal error in game loop: {str(e)}")
            self.display_text(f"A fatal error occurred: {str(e)}\nThe game will now exit.")
            time.sleep(3)
            self.running = False

    def display_status_bar(self):
        """Display status bar in the GUI"""
        if hasattr(self, 'current_location') and self.current_location:
            location_name = self.current_location.name
        else:
            location_name = "Unknown Location"
        
        self.gui.update_status(
            title="THE DEEP",
            health=self.player.health,
            location=location_name
        )
        logger.debug(f"Updated status bar - Health: {self.player.health}, Location: {location_name}")

    def get_player_input(self, prompt="\nWhat would you like to do? > ", options=None):
        """Get player input using the GUI and keyboard"""
        # Display the prompt in the GUI text area
        self.gui.display_text(prompt)
        
        if options:
            self.current_options = options
            self.gui.set_menu_options(options)
            self.selecting_menu_option = True
            logger.debug(f"Displaying {len(options)} menu options")
            
            # Configure GUI to handle menu selection
            self.gui.enable_menu_selection()
            
            # Wait for user to select an option
            self.input_ready = False
            self.input_value = None
            
            def on_selection(selection):
                self.input_value = selection
                self.input_ready = True
                self.selecting_menu_option = False
            
            self.gui.set_selection_callback(on_selection)
            
            # Ensure focus is on the listbox, not the text area
            self.root.after(100, self.gui.set_focus_to_menu)
            
            # Wait for selection
            while not self.input_ready and self.running:
                self.root.update()
                time.sleep(0.05)
            
            self.gui.disable_menu_selection()
            return self.input_value
        else:
            # For free text input
            self.input_ready = False
            self.input_value = None
            
            # Create an entry field in the GUI
            self.gui.show_input_field(prompt)
            
            def on_input_submit(text):
                self.input_value = text
                self.input_ready = True
            
            self.gui.set_input_callback(on_input_submit)
            
            # Wait for input
            while not self.input_ready and self.running:
                self.root.update()
                time.sleep(0.05)
                
            self.gui.hide_input_field()
            return self.input_value
            
    def wait_for_menu_selection(self):
        """Wait for the user to select a menu option using keyboard"""
        self.selecting_menu_option = True
        selected_option = None
        
        def on_enter_or_space(event=None):
            nonlocal selected_option
            selected_option = self.current_options[self.gui.selected_option]
            self.selecting_menu_option = False
        
        # Bind enter/space to selection
        self.root.bind("<Return>", on_enter_or_space)
        self.root.bind("<space>", on_enter_or_space)
        
        # Wait for selection
        while self.selecting_menu_option:
            self.root.update()
            time.sleep(0.1)
        
        # Unbind to prevent duplicate handlers
        self.root.unbind("<Return>")
        self.root.unbind("<space>")
        
        logger.debug(f"Selected option: {selected_option}")
        return selected_option
    
    def handle_player_input(self):
        """Get and process player input through the GUI"""
        try:
            # First determine available actions based on current location
            available_actions = self.get_available_actions()
            
            # Present options to player using the GUI menu
            action = self.get_player_input("\nWhat would you like to do? > ", available_actions)
            
            if not action:
                return  # No action selected, skip processing
                
            logger.debug(f"Player chose action: {action}")
            
            # Process the selected action
            if action.startswith("Move"):
                direction = action.split("(")[1].split(")")[0]
                self.move_player(direction)
            elif action == "Inventory":
                inventory_text = self.player.show_inventory()
                self.display_text(inventory_text)
                time.sleep(2)  # Give user time to read
            elif action == "Look around":
                self.display_text(self.current_location.description)
                if self.current_location.items:
                    self.display_text("\nYou notice:")
                    for item in self.current_location.items:
                        self.display_text(f"- {item.name}")
                time.sleep(1.5)
            elif action == "Journal":
                journal_text = self.player.read_journal()
                self.display_text(journal_text)
                time.sleep(2)
            elif action == "Samples":
                samples_text = self.player.view_samples()
                self.display_text(samples_text)
                time.sleep(2)
            elif action.startswith("Examine"):
                item = action.replace("Examine ", "")
                self.examine_item(item)
            elif action.startswith("Take"):
                item_name = action.replace("Take ", "")
                self.take_item(item_name)
            elif action.startswith("Use"):
                item_name = action.replace("Use ", "")
                self.use_item(item_name)
            elif action == "Objectives":
                self.show_objectives()
            elif action == "Help":
                self.show_help()
            elif action == "Quit":
                confirm = self.get_player_input("Are you sure you want to quit? (y/n) ")
                if confirm.lower() == "y":
                    self.game_running = False
                    logger.info("Player chose to quit")
                    self.root.after(1000, self.root.destroy)
        except Exception as e:
            logger.error(f"Error processing player input: {str(e)}")
            self.display_text(f"Error processing your action: {str(e)}\nPlease try something else.")
            time.sleep(2)
    
    def handle_combat(self):
        """Handle combat encounters in GUI mode without color codes"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
        
        enemy = self.current_enemy
        
        # Display combat information without color codes
        self.display_text(f"\nCOMBAT: {enemy.name} attacks!")
        self.display_text(f"Enemy health: {enemy.health}/{enemy.max_health}")
        
        # Add fallback for threat_level if it doesn't exist
        threat_level = getattr(enemy, 'threat_level', 0.5)  # Default to medium threat
        self.display_text(f"Threat level: {threat_level}")
        self.display_text(enemy.description)
        
        # Offer combat options
        combat_actions = [
            "Attack",
            "Use item",
            "Try to flee"
        ]
        
        action = self.get_player_input("\nWhat will you do? > ", combat_actions)
        
        if action == "Attack":
            # Player attacks enemy
            damage = self.player.attack()
            
            # Display weapon info if equipped
            weapon_text = ""
            if hasattr(self.player, 'equipped_weapon') and self.player.equipped_weapon:
                weapon_text = f" using your {self.player.equipped_weapon.name}"
            
            enemy.health -= damage
            self.display_text(f"\nYou attack the {enemy.name}{weapon_text} for {damage} damage!")
            
            # Update GUI with new enemy health
            self.display_status_bar()
            
            if not enemy.is_alive():
                self.handle_enemy_defeat(enemy)
                return
            
        elif action == "Use item":
            # Let player select an item to use
            if not self.player.inventory:
                self.display_text("\nYou don't have any items to use.")
                return
                
            item_options = [item.name for item in self.player.inventory]
            item_options.append("Cancel")
            
            selected_item = self.get_player_input("\nWhich item will you use? > ", item_options)
            
            if selected_item == "Cancel":
                # Return to combat menu
                return
                
            # Find and use the selected item
            for item in self.player.inventory:
                if item.name == selected_item:
                    self.use_item(item.name)
                    break
            
        elif action == "Try to flee":
            # Chance to escape based on enemy threat
            # Add fallback for threat_level if it doesn't exist
            threat_level = getattr(enemy, 'threat_level', 0.5)
            escape_chance = 0.8 - (threat_level * 0.1)
            if random.random() < escape_chance:
                self.display_text(f"\nYou successfully escape from the {enemy.name}!")
                self.current_enemy = None
                # Reset combat state
                return
            else:
                self.display_text(f"\nYou fail to escape from the {enemy.name}!")
        
        # Enemy attacks player if still alive
        if self.current_enemy and self.current_enemy.is_alive():
            enemy_damage = enemy.attack()
            self.player.health -= enemy_damage
            self.display_text(f"\nThe {enemy.name} attacks you for {enemy_damage} damage!")
            
            # Update GUI with new player health
            self.display_status_bar()
            
            if self.player.health <= 0:
                self.display_text("\nYou have been defeated...")
                self.game_over("You have succumbed to the depths...")
    
    def display_ascii_art(self, art_file):
        """Display ASCII art in the GUI"""
        from ui.ascii_art import load_ascii_art
        
        art = load_ascii_art(art_file)
        if art:
            print(art)
            logger.debug(f"Displayed ASCII art: {art_file}")
        else:
            logger.warning(f"Could not load ASCII art: {art_file}")
            
    def typewriter_text(self, text, delay=0.05):
        """Display text with typewriter effect in GUI"""
        print_typing_effect(text, delay)
        logger.debug("Displayed text with typewriter effect")
    
    # Fix the display_text method to handle color codes properly
    def display_text(self, text):
        """Display text in the GUI with proper formatting"""
        # Replace ANSI color codes with empty strings for GUI display
        if text:
            try:
                # Handle all potential ANSI color codes
                ansi_codes = [
                    "\033[0m",  # Reset
                    "\033[1m",  # Bold
                    "\033[31m", # Red
                    "\033[32m", # Green
                    "\033[33m", # Yellow
                    "\033[34m", # Blue
                    "\033[35m", # Magenta
                    "\033[36m", # Cyan
                    "\033[37m", # White
                    "\033[90m", # Bright Black (Gray)
                    "\033[91m", # Bright Red
                    "\033[92m", # Bright Green
                    "\033[93m", # Bright Yellow
                    "\033[94m", # Bright Blue
                    "\033[95m", # Bright Magenta
                    "\033[96m", # Bright Cyan
                    "\033[97m"  # Bright White
                ]
                
                # Remove all ANSI codes
                for code in ansi_codes:
                    text = text.replace(code, "")
                    
                # Also handle the named colors from the Colors class
                if '{Colors.RED}' in text: text = text.replace('{Colors.RED}', '')
                if '{Colors.GREEN}' in text: text = text.replace('{Colors.GREEN}', '')
                if '{Colors.YELLOW}' in text: text = text.replace('{Colors.YELLOW}', '')
                if '{Colors.BLUE}' in text: text = text.replace('{Colors.BLUE}', '')
                if '{Colors.MAGENTA}' in text: text = text.replace('{Colors.MAGENTA}', '')
                if '{Colors.CYAN}' in text: text = text.replace('{Colors.CYAN}', '')
                if '{Colors.BOLD}' in text: text = text.replace('{Colors.BOLD}', '')
                if '{Colors.RESET}' in text: text = text.replace('{Colors.RESET}', '')
                
                # Use regex for any remaining ANSI escape sequences
                import re
                text = re.sub(r'\033\[\d+(;\d+)?m', '', text)
                
            except Exception as e:
                # Log the error but continue with the original text
                logger.error(f"Error processing color codes: {str(e)}")
        
        # Send the cleaned text to the GUI
        self.gui.display_text(text)

    def display_intro(self):
        """Display game introduction in the GUI with better formatting"""
        # Use the built-in title display function from ascii_art
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
        self.gui.display_text(title_art)
        
        # Use better formatted text with line breaks
        intro_text = """
        Welcome to THE DEEP, an educational adventure game about deep-sea exploration.
        
        You are a marine biologist embarking on a journey to study the mysterious 
        ecosystems of the deep ocean. Your mission is to collect samples and document 
        the strange phenomena occurring beneath the waves.
        """
        self.gui.display_text(intro_text)
        self.wait_for_player_continue()
        
    def display_mission_briefing(self):
        """Display the mission briefing with better formatting"""
        briefing = """
        === MISSION BRIEFING ===
        
        Recent reports indicate unusual activity in the deep ocean trenches. 
        
        Marine life has been behaving strangely, and satellite imagery shows 
        unexplained thermal anomalies in several locations. Your mission is to:
        
        1. Explore the deep ocean environments
        2. Document unusual phenomena and lifeforms
        3. Collect biological and water samples
        4. Investigate the source of the thermal anomalies
        
        Your research vessel is equipped with state-of-the-art diving equipment and 
        scientific instruments. The safety of you and your team is paramount.
        
        Good luck, and remember - in the deep, you're never truly alone.
        """
        self.gui.display_text(briefing)
        self.wait_for_player_continue()

    def wait_for_player_continue(self):
        """Wait for player to press a key to continue"""
        # Don't use color codes here to avoid issues
        self.gui.display_text("\nPress ENTER to continue...")
        
        self.input_ready = False
        
        # Simple callback function
        def on_continue_key(event=None):
            self.input_ready = True
        
        # Set the callback in the GUI
        self.gui.set_continue_callback(on_continue_key)
        
        # Wait for input
        while not self.input_ready and self.running:
            self.root.update()
            time.sleep(0.05)
        
        # Re-bind keys after the continue prompt
        self.root.bind("<Up>", self.gui.handle_up)
        self.root.bind("<Down>", self.gui.handle_down)
        self.root.bind("<Return>", self.gui.handle_select)
        self.root.bind("<space>", self.gui.handle_select)
        
        # Small delay to prevent immediate trigger of the next input
        time.sleep(0.2)
    
    def take_item(self, item_name):
        """Pick up an item from the current location"""
        # Find the item in the current location
        item_to_take = None
        for item in self.current_location.items:
            if item.name.lower() == item_name.lower():
                item_to_take = item
                break
        
        if not item_to_take:
            # Display message for longer time
            message = f"There is no {item_name} here to take."
            self.display_text(message)
            time.sleep(1.5)  # Pause to ensure message is seen
            return
        
        # Remove item from location and add to inventory
        self.current_location.items.remove(item_to_take)
        self.player.inventory.append(item_to_take)
        
        # Show success message
        success_message = f"You take the {item_to_take.name}."
        if hasattr(item_to_take, 'on_pickup_message') and item_to_take.on_pickup_message:
            success_message += f"\n{item_to_take.on_pickup_message}"
        self.display_text(success_message)
        time.sleep(1)  # Pause to ensure message is seen

    def game_over(self, message):
        """Handle game over state with a proper ending"""
        self.display_text(f"\n{message}")
        time.sleep(2)
        
        if self.player.health <= 0:
            # Bad ending
            ending_text = """
            Your vision fades as the cold depths claim you. The last thing you see is the 
            strange bioluminescence of the deep sea creatures surrounding you.

            Your research and samples are never recovered, and the mysteries of The Deep 
            remain unsolved. Perhaps another brave soul will continue your work someday...

            GAME OVER - You have failed to survive The Deep.
            """
        else:
            # Good or neutral ending depending on samples collected
            sample_count = len(self.player.samples)
            if sample_count >= 5:
                ending_text = """
                With your extensive collection of samples and documentation of The Deep's 
                corruption, you return to the surface as a hero. Your evidence leads to 
                international action against ocean pollution and the mysterious entity 
                known as the Tidecaller retreats to the deepest trenches.

                Your name goes down in scientific history, and the oceans begin their 
                long process of healing thanks to your brave expedition.

                CONGRATULATIONS - You've successfully completed your mission!
                """
            else:
                ending_text = """
                You've survived your expedition to The Deep, returning with some valuable 
                samples but not enough to make a conclusive case about what's happening below.

                Your findings spark interest in the scientific community, but without more 
                substantial evidence, the polluters continue their activities. Perhaps a 
                future expedition will uncover the full truth.

                GAME OVER - You've survived, but your mission remains incomplete.
                """

        self.display_text(ending_text)
        time.sleep(5)  # Give player time to read the ending

        # Ask if player wants to play again
        play_again = self.get_player_input("\nWould you like to play again? (y/n): ")
        if play_again and play_again.lower() == "y":
            self.restart_game()
        else:
            self.running = False
            self.root.after(1000, self.root.destroy)

    def restart_game(self):
        """Restart the game from the beginning"""
        # Reset player stats
        self.player.health = self.player.max_health
        self.player.inventory = []
        self.player.samples = []
        self.player.journal = []
        
        # Reset game state
        self.game_state = GameState()
        self.current_location = self.game_state.current_location
        
        # Set player location
        if hasattr(self.player, 'set_location'):
            self.player.set_location(self.current_location)
            
        # Reset combat variables
        self.current_enemy = None
        self.steps_since_combat = 0
        
        # Start fresh
        self.display_status_bar()
        self.display_text("\n\n--- NEW GAME ---\n\n")
        self.display_intro()
        self.display_mission_briefing()
        self.display_status_bar()
        self.display_text("\n\n--- NEW GAME ---\n\n")
        self.display_intro()
        self.display_mission_briefing()
        
        # Start fresh
        self.display_status_bar()
        self.display_text("\n\n--- NEW GAME ---\n\n")
        self.display_intro()
        self.display_mission_briefing()
        self.player.inventory = []
        self.player.samples = []
        self.player.journal = []
        
        # Reset game state
        self.game_state = GameState()
        self.current_location = self.game_state.current_location
        self.current_enemy = None
        self.steps_since_combat = 0
        
        # Start fresh
        self.display_status_bar()
        self.display_text("\n\n--- NEW GAME ---\n\n")
        self.display_intro()
        self.display_mission_briefing()

    def process_current_location(self):
        """Process the current location and display information without color codes."""
        if not self.current_location:
            # Set initial location if none exists
            from world.locations import get_starting_location
            self.current_location = get_starting_location()
            self.player.set_location(self.current_location.id)

        # Check if this is the first visit to show detailed description
        first_visit = not self.current_location.visited
        self.current_location.visited = True
        
        # Display location information without color codes
        self.display_text(f"\n=== {self.current_location.name} ===\n")
        
        if first_visit:
            self.display_text(f"{self.current_location.description}\n")
            
            # Educational content on first visit (without color codes)
            if "reef" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: Coral reefs are among the most diverse ecosystems on Earth, but pollution, climate change, and ocean acidification have led to a 50% decline in coral reefs worldwide in the past 30 years.\n")
            elif "trench" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: The deep ocean remains one of the least explored regions on Earth. Deep sea trenches can reach depths exceeding 36,000 feet, where pressure is more than 1,000 times that at sea level.\n")
            elif "bloom" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: Algal blooms can create hypoxic conditions (low oxygen) that lead to 'dead zones' where marine life cannot survive. The largest dead zone in the world is in the Baltic Sea.\n")
            
            # Add journal entry for first visit
            if hasattr(self.player, 'add_journal_entry'):
                self.player.add_journal_entry(f"Visited {self.current_location.name}. {self.current_location.description[:100]}...")
        else:
            # Shorter description for return visits
            self.display_text(f"You are back at {self.current_location.name}.\n")
            
        # Display any items in the location
        if self.current_location.items:
            self.display_text("\nYou notice:")
            for item in self.current_location.items:
                self.display_text(f"- {item.name}")
        # Always display available exits
        if self.current_location.exits:
            self.display_text("\nPossible directions:")
            for direction in self.current_location.exits:
                self.display_text(f"- {direction}")
        # Display location information without color codes
        self.display_text(f"\n=== {self.current_location.name} ===\n")
        
        if first_visit:
            self.display_text(f"{self.current_location.description}\n")
            
            # Educational content on first visit (without color codes)
            if "reef" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: Coral reefs are among the most diverse ecosystems on Earth, but pollution, climate change, and ocean acidification have led to a 50% decline in coral reefs worldwide in the past 30 years.\n")
            elif "trench" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: The deep ocean remains one of the least explored regions on Earth. Deep sea trenches can reach depths exceeding 36,000 feet, where pressure is more than 1,000 times that at sea level.\n")
            elif "bloom" in self.current_location.id:
                self.display_text("\nEDUCATIONAL NOTE: Algal blooms can create hypoxic conditions (low oxygen) that lead to 'dead zones' where marine life cannot survive. The largest dead zone in the world is in the Baltic Sea.\n")
            
            # Add journal entry for first visit
            if hasattr(self.player, 'add_journal_entry'):
                self.player.add_journal_entry(f"Visited {self.current_location.name}. {self.current_location.description[:100]}...")
        else:
            # Shorter description for return visits
            self.display_text(f"You are back at {self.current_location.name}.\n")
            
        # Display any items in the location
        if self.current_location.items:
            self.display_text("\nYou notice:")
            for item in self.current_location.items:
                self.display_text(f"- {item.name}")
        # Always display available exits
        if self.current_location.exits:
            self.display_text("\nPossible directions:")
            for direction in self.current_location.exits:
                self.display_text(f"- {direction}")
