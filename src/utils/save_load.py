def save_game(game_state, filename='save_file.json'):
    import json

    with open(filename, 'w') as f:
        json.dump(game_state, f)
    print("Game saved successfully.")

def load_game(filename='save_file.json'):
    import json

    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)
        print("Game loaded successfully.")
        return game_state
    except FileNotFoundError:
        print("Save file not found. Starting a new game.")
        return None
    except json.JSONDecodeError:
        print("Error loading save file. It may be corrupted.")
        return None