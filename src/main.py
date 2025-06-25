"""
Main entry point for The Deep game.
Now exclusively runs in GUI mode.
"""

import sys
import os
import logging
import tkinter as tk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("game_log.txt", mode='w')
    ]
)
logger = logging.getLogger('the_deep.main')

# Add src directory to path to ensure imports work
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

def main():
    """Main function to start the game in GUI mode"""
    try:
        # Create a simple splash screen
        splash = tk.Tk()
        splash.title("The Deep - Loading...")
        splash.geometry("400x200")
        splash.configure(bg="#000033")
        
        # Center the splash screen
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        splash.geometry(f"400x200+{x}+{y}")
        
        # Add loading text
        label = tk.Label(
            splash, 
            text="THE DEEP\nLoading...", 
            font=("Courier", 16, "bold"),
            bg="#000033",
            fg="white"
        )
        label.pack(expand=True)
        splash.update()
        
        # Import modules after setting up paths
        from game.player import Player
        from game.gui_engine import GUIGameEngine
        
        # Get player name using a simple GUI dialog
        def submit_name():
            global player_name
            player_name = name_entry.get()
            if not player_name:
                player_name = "Explorer"
            splash.destroy()
            
        name_frame = tk.Frame(splash, bg="#000033")
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        name_label = tk.Label(
            name_frame, 
            text="Enter your name:", 
            bg="#000033", 
            fg="white",
            font=("Courier", 12)
        )
        name_label.pack(side=tk.TOP, pady=5)
        
        name_entry = tk.Entry(name_frame, font=("Courier", 12), bg="#001144", fg="white")
        name_entry.pack(side=tk.TOP, fill=tk.X, pady=5)
        name_entry.focus_set()
        
        submit_button = tk.Button(
            name_frame, 
            text="Start Adventure", 
            command=submit_name,
            bg="#001144",
            fg="white",
            font=("Courier", 12)
        )
        submit_button.pack(side=tk.TOP, pady=5)
        
        # Add Enter key binding
        splash.bind("<Return>", lambda e: submit_name())
        
        # Global variable to store player name
        global player_name
        player_name = "Explorer"  # Default
        
        # Wait for user input
        splash.mainloop()
        
        # Start the game
        player = Player(name=player_name)
        engine = GUIGameEngine(player)
        engine.start()
            
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        print(f"\nError: Could not start the game due to missing modules.")
        print(f"Details: {str(e)}")
        print("\nPlease make sure all required packages are installed.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\nAn unexpected error occurred: {str(e)}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()