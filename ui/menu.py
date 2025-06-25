class Menu:
    def __init__(self, options):
        self.options = options
        self.selected_index = 0

    def display(self):
        print("\n" + self.get_title())
        for index, option in  enumerate(self.options):
            if index == self.selected_index:
                print(f"> {option}")
            else:
                print(f"  {option}")
    
    def get_title(self):
        return "🧭 Main Menu"

    def navigate(self, direction):
        if direction == "up":
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif direction == "down":
            self.selected_index = (self.selected_index + 1) % len(self.options)
        else:
            print("Invalid navigation direction. Use 'up' or 'down'.")

    def select(self):
        return self.options[self.selected_index]