"""
GUI for inputting item name for Smart Bin project.

Displays On-Screen keyboard, Input Box, and Submit button for finding correct
bin to place item into.

Todo:
- Add feedback for inputted item (error if doesn't exist)

@Author: Patrick Roe, http://pproe.dev
@Date: 12/09/2022
"""

import tkinter as tk
from backend import Backend
from keyboard import Keyboard


class App(tk.Frame):
    """Main TKinter GUI for item lookup for the Smart Bin project"""

    def __init__(self, parent, *args, **kwargs):
        """Initialise GUI and all of its components."""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.backend = Backend(self)

        # Setup Keyboard
        self.keyboard = Keyboard(self, bg="cornflowerblue")
        self.keyboard.pack()


if __name__ == "__main__":
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
