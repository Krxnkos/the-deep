"""
GUI module for The Deep game.
Creates a tkinter window for the game while keeping debugging output in the terminal.
"""
import tkinter as tk
from tkinter import scrolledtext, font
import sys
import queue
import threading
import logging
import time

# Configure logging to show in terminal
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('the_deep')

class StdoutRedirector:
    """Redirects stdout to both the terminal and the GUI"""
    def __init__(self, text_widget):
        self.terminal = sys.stdout
        self.text_widget = text_widget
        self.queue = queue.Queue()
        
    def write(self, message):
        self.terminal.write(message)  # Write to terminal
        self.queue.put(message)       # Queue for GUI thread
        
    def flush(self):
        self.terminal.flush()

class GameGUI:
    """Main GUI class for The Deep game"""
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.root.title("THE DEEP")
        self.root.geometry("800x600")
        self.root.configure(bg="#000033")  # Dark blue background
        
        # Create custom fonts
        self.title_font = font.Font(family="Courier", size=16, weight="bold")
        self.text_font = font.Font(family="Courier", size=12)
        
        # Create frame for status bar
        self.status_frame = tk.Frame(self.root, bg="#000022", height=40)
        self.status_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Status elements
        self.title_label = tk.Label(
            self.status_frame, 
            text="THE DEEP", 
            font=self.title_font, 
            fg="white", 
            bg="#000022",
            anchor="w"
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.health_label = tk.Label(
            self.status_frame,
            text="Health: 100", 
            font=("Arial", 10),
            fg="white", 
            bg="#000022"
        )
        self.health_label.pack(side=tk.RIGHT, padx=10)
        
        self.location_label = tk.Label(
            self.status_frame,
            text="Location: Unknown", 
            font=("Arial", 10),
            fg="white", 
            bg="#000022"
        )
        self.location_label.pack(side=tk.RIGHT, padx=10)
        
        # Create main text area with scrolling
        self.text_frame = tk.Frame(self.root, bg="#000033")
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_area = scrolledtext.ScrolledText(
            self.text_frame, wrap=tk.WORD,
            bg="#000033", fg="white",
            font=("Courier", 11),
            insertbackground="white"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)  # Read only
        
        # Prevent text area from capturing arrow key focus
        self.text_area.bind("<Up>", lambda e: "break")
        self.text_area.bind("<Down>", lambda e: "break")
        self.text_area.bind("<Left>", lambda e: "break")
        self.text_area.bind("<Right>", lambda e: "break")
        
        # Create menu options frame
        self.menu_frame = tk.Frame(self.root, bg="#000022", height=150)
        self.menu_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Menu options list
        self.options_listbox = tk.Listbox(
            self.menu_frame, bg="#000022", fg="white",
            font=("Courier", 11), selectbackground="#003366",
            selectforeground="white", height=6
        )
        self.options_listbox.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Input field (initially hidden)
        self.input_frame = tk.Frame(self.menu_frame, bg="#000022")
        self.input_entry = tk.Entry(
            self.input_frame, bg="#000033", fg="white",
            font=("Courier", 11), insertbackground="white"
        )
        self.input_button = tk.Button(
            self.input_frame, text="Submit", 
            bg="#003366", fg="white",
            command=self._on_input_submit
        )
        self.input_frame.pack_forget()  # Hidden by default
        
        # Store current state
        self.selected_option = 0
        self.menu_options = []
        self.menu_labels = []
        self.menu_selection_enabled = False
        self.selection_callback = None
        self.input_callback = None
        self.continue_callback = None
        
        # Set up stdout redirection
        self.stdout_redirector = StdoutRedirector(self.text_area)
        sys.stdout = self.stdout_redirector
        
        # Start a thread to process the queue
        self.update_queue()
        
        # Key bindings for navigation
        self.root.bind("<Up>", self.handle_up)
        self.root.bind("<Down>", self.handle_down)
        self.root.bind("<Return>", self.handle_select)
        self.root.bind("<space>", self.handle_select)
        
        logger.info("GUI initialized")
        
    def update_queue(self):
        """Process any stdout messages in the queue and update the text widget"""
        try:
            while True:
                message = self.stdout_redirector.queue.get_nowait()
                self.update_text_area(message)
        except queue.Empty:
            pass
        self.root.after(100, self.update_queue)
        
    def update_text_area(self, message):
        """Update the text area with new text"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        
    def clear_text_area(self):
        """Clear the text area"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
        
    def update_status(self, title, health, location):
        """Update the status bar with player info"""
        if title:
            self.title_label.config(text=title)
        if health is not None:
            self.health_label.config(text=f"Health: {health}")
        if location:
            self.location_label.config(text=f"Location: {location}")
            
    def display_text(self, text):
        """Display text in the main text area with improved formatting"""
        if not text:
            return
        
        self.text_area.config(state=tk.NORMAL)
        
        # Add extra line breaks for readability
        if text.strip():
            # Make sure text has proper spacing
            if not text.endswith("\n"):
                text += "\n"
            
            # Add the text
            self.text_area.insert(tk.END, text)
            
            # Add a visual separator for longer texts
            if len(text.strip()) > 200:  # Only for substantial text blocks
                self.text_area.insert(tk.END, "\n")
        
        self.text_area.see(tk.END)  # Auto-scroll to the bottom
        self.text_area.config(state=tk.DISABLED)
        self.root.update()  # Force update to show text immediately
        logger.debug(f"Displayed text: {text[:30]}...")
        
    def clear_text(self):
        """Clear the text area"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
        
    def set_menu_options(self, options):
        """Set the available menu options"""
        self.menu_options = options
        self.options_listbox.delete(0, tk.END)
        for option in options:
            self.options_listbox.insert(tk.END, option)
        
        # Select the first option by default
        self.selected_option = 0
        self.options_listbox.selection_set(0)
        self.options_listbox.see(0)
        
    def set_focus_to_menu(self):
        """Set focus to the menu options listbox to ensure arrow keys work properly"""
        if self.menu_selection_enabled:
            self.options_listbox.focus_set()
    
    def enable_menu_selection(self):
        """Enable menu selection mode"""
        self.menu_selection_enabled = True
        self.input_frame.pack_forget()
        self.options_listbox.pack(fill=tk.BOTH, padx=10, pady=10)
        self.set_focus_to_menu()  # Set focus to menu when enabled
        
    def disable_menu_selection(self):
        """Disable menu selection mode"""
        self.menu_selection_enabled = False
        
    def show_input_field(self, prompt=None):
        """Show the text input field"""
        if prompt:
            self.display_text(prompt)
            
        self.options_listbox.pack_forget()
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_button.pack(side=tk.RIGHT)
        
        # Focus on input field
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()
        
    def hide_input_field(self):
        """Hide the text input field"""
        self.input_frame.pack_forget()
        self.options_listbox.pack(fill=tk.BOTH, padx=10, pady=10)
        
    def set_selection_callback(self, callback):
        """Set callback for menu selection"""
        self.selection_callback = callback
        
    def set_input_callback(self, callback):
        """Set callback for text input"""
        self.input_callback = callback
        
    def set_continue_callback(self, callback):
        """Set callback for continue prompt"""
        self.continue_callback = callback
        
        # Store current bindings to restore later
        self._temp_old_bindings = {
            "Up": self.root.bind("<Up>"),
            "Down": self.root.bind("<Down>"),
            "Return": self.root.bind("<Return>"),
            "space": self.root.bind("<space>")
        }
        
        # Unbind current keys
        for key in self._temp_old_bindings:
            self.root.unbind(f"<{key}>")
        
        # Set specific bindings for continue prompt
        self.root.bind("<Return>", lambda e: callback())
        self.root.bind("<space>", lambda e: callback())
        
        # Add a visual indicator for the continue prompt
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, "\n▼ Press ENTER or SPACE to continue ▼\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        
    def handle_up(self, event):
        """Handle up arrow key"""
        if not self.menu_options:
            return "break"  # Prevent event propagation
        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        self.update_menu_selection()
        logger.debug(f"Selected option: {self.selected_option}")
        return "break"  # Prevent event propagation
        
    def handle_down(self, event):
        """Handle down arrow key"""
        if not self.menu_options:
            return "break"  # Prevent event propagation
        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        self.update_menu_selection()
        logger.debug(f"Selected option: {self.selected_option}")
        return "break"  # Prevent event propagation
        
    def update_menu_selection(self):
        """Update the visual selection in the menu options list"""
        self.options_listbox.selection_clear(0, tk.END)
        self.options_listbox.selection_set(self.selected_option)
        self.options_listbox.see(self.selected_option)
        self.options_listbox.activate(self.selected_option)
        self.root.update()
        
    def handle_select(self, event):
        """Handle enter or space key"""
        if not self.menu_options or not self.menu_selection_enabled:
            return
        
        selected = self.menu_options[self.selected_option]
        logger.debug(f"Option selected: {selected}")
        
        if self.selection_callback:
            self.selection_callback(selected)
        return selected
        
    def show_message(self, message, duration=2.0):
        """Show a message in the text area with a minimum display time"""
        self.update_text_area(f"{message}\n")
        # Update immediately and wait to ensure visibility
        self.root.update()
        time.sleep(duration)
        
    def _on_input_submit(self):
        """Handle input submission from the input field"""
        if self.input_callback:
            text = self.input_entry.get()
            self.input_callback(text)
        else:
            # If no callback is set, just clear the input field
            self.input_entry.delete(0, tk.END)
        
    def run(self):
        """Start the tkinter main loop"""
        self.root.mainloop()
