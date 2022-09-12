"""
GUI for inputting item name for Smart Bin project.

Displays On-Screen keyboard, Input Box, and Submit button for finding correct
bin to place item into.

Todo:
- Add feedback for inputted item (error if doesn't exist)

@Author: Patrick Roe, http://pproe.dev
@Date: 12/09/2022
"""

from cgitb import text
import tkinter as tk
from turtle import bgcolor
from backend import Backend
from keyboard import Keyboard


# Configuration Options
BACKGROUND_COLOUR = "white"


class App(tk.Frame):
    """Main TKinter GUI for item lookup for the Smart Bin project"""

    def __init__(self, parent, *args, **kwargs):
        """Initialise GUI and all of its components."""
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOUR, *args, **kwargs)
        self.parent = parent
        self.backend = Backend(self)

        self.input_frame = tk.Frame(self, bg=BACKGROUND_COLOUR)

        # String variable for input box
        input_text = tk.StringVar()

        # Setup Label tooltip
        self.tooltip = tk.Label(
            self, text="Scan Barcode or enter product name below:"
        )

        # Setup Input Box & Button
        self.input_box = tk.Entry(
            self.input_frame,
            textvariable=input_text,
            highlightcolor="black",
            highlightthickness=1,
        )
        self.input_box.focus()
        self.submit_button = tk.Button(
            self.input_frame, text="Submit", bg=BACKGROUND_COLOUR
        )

        # Setup Keyboard
        self.keyboard = Keyboard(self, bg=BACKGROUND_COLOUR)

        # Build Layout
        self.tooltip.pack(side=tk.TOP, pady=25)
        self.input_frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.X)
        self.input_box.pack(
            side=tk.LEFT, fill=tk.X, expand=tk.TRUE, padx=25, pady=10
        )
        self.submit_button.pack(side=tk.LEFT, padx=25, pady=10)
        self.keyboard.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.FALSE)


if __name__ == "__main__":
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
