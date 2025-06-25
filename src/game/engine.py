class GameEngine:
    def __init__(self):
        self.running = True
        self.game_state = None
        self.player = None

    def start_game(self):
        self.initialise_game_state()
        self.main_game_loop()

    def initialise_game_state(self):
        from game.game_state import GameState
        from game.player import Player

        self.game_state = GameState()
        self.player = Player()

    def main_game_loop(self):
        while self.running:
            self.process_input()
            self.update_game_state()
            self.render()
    
    def handle_input(self):
        user_input = input("Enter command: ")
        if user_input.lower() in ['exit', 'quit']:
            self.running = False
        else:
            self.process_command(user_input)
            # print(f"Processing command: {user_input}")
    
    def process_command(self, command):
        # Placeholder for command processing logic
        print(f"Command '{command}' processed.")
    
    def update_game_state(self):
        # Placeholder for game state update logic
        pass

    def render(self):

        # Placeholder for rendering logic
        print("Rendering game state...")