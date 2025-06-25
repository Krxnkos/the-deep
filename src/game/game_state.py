class GameState:
    def __init__(self):
        self.player_health = 100
        self.inventory = []
        self.current_location = None
        self.story_progress = 0

    def update_health(self, amount):
        self.player_health += amount
        if self.player_health >100:
            self.player_health = 100
        elif self.player_health <= 0:
            self.player_health = 0
            self.game_over()
    
    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            print(f"Item '{item}' not found in inventory.")
    
    def set_location(self, location):
        self.current_location = location
    
    def game_over(self):
        print("Game Over! You have succumbed to the horros of the deep!")
        # Additional game over logic can be added here, such as resetting the game or showing a game over screen.

    def progress_story(self, amount):
        self.story_progress += 1
        # Additional logic for story progression can be added here, such as triggering events or changing locations.