import tkinter as tk
import pyautogui

# ========== Configurations ====================
BUTTON_BACKGROUND = "white"
MAIN_FRAME_BACKGROUND = "cornflowerblue"
BUTTON_LOOK = "flat"  # flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE = "Python Virtual KeyBoard."
TOPBAR_BACKGROUND = "skyblue"
TRANSPARENCY = 1
FONT_COLOR = "black"

# ==============================================

keys = [
    [
        # =========================================
        # ===== Keyboard Configurations ===========
        # =========================================
        [
            ("Character_Keys"),
            ({"side": "top", "expand": "yes", "fill": "both"}),
            [
                ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "backspace"),
                (
                    "tab",
                    "q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                    "{",
                    "}",
                    ";",
                    "'",
                ),
                (
                    "capslock",
                    "a",
                    "s",
                    "d",
                    "f",
                    "g",
                    "h",
                    "j",
                    "k",
                    "l",
                    ":",
                    '"',
                    "enter",
                ),
                (
                    "shift",
                    "z",
                    "x",
                    "c",
                    "v",
                    "b",
                    "n",
                    "m",
                    "<",
                    ">",
                    "?",
                    "shift",
                ),
            ],
        ],
    ],
]

##  Frame Class
class Keyboard(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Function For Creating Buttons
        self.create_frames_and_buttons()

    # Function For Extracting Data From KeyBoard Table and generating GUI
    def create_frames_and_buttons(self):
        # take section one by one
        for key_section in keys:
            # create Sperate Frame For Every Section
            store_section = tk.Frame(self)
            store_section.pack(
                side="left",
                expand="yes",
                fill="both",
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )

            for layer_name, layer_properties, layer_keys in key_section:
                store_layer = tk.LabelFrame(store_section)  # , text=layer_name)
                # store_layer.pack(side='top',expand='yes',fill='both')
                store_layer.pack(layer_properties)
                for key_bunch in layer_keys:
                    store_key_frame = tk.Frame(store_layer)
                    store_key_frame.pack(side="top", expand="yes", fill="both")
                    for k in key_bunch:
                        k = k.capitalize()
                        if len(k) <= 3:
                            store_button = tk.Button(
                                store_key_frame, text=k, width=2, height=2
                            )
                        else:
                            store_button = tk.Button(
                                store_key_frame, text=k.center(5, " "), height=2
                            )
                        if " " in k:
                            store_button["state"] = "disable"

                        store_button["relief"] = BUTTON_LOOK
                        store_button["bg"] = BUTTON_BACKGROUND
                        store_button["fg"] = FONT_COLOR

                        store_button[
                            "command"
                        ] = lambda q=k.lower(): self.button_command(q)
                        store_button.pack(
                            side="left", fill="both", expand="yes"
                        )
        return

        # Function For Detecting Pressed Keyword.

    def button_command(self, event):
        pyautogui.press(event)
        return


# Creating Main Window
def main():
    root = tk.Tk(className=TOP_BAR_TITLE)
    k = Keyboard(root, bg=MAIN_FRAME_BACKGROUND)

    # Confifuration
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes("-alpha", TRANSPARENCY)
    # Custum
    f = tk.Frame(root)
    t_bar = tk.Label(f, text=TOP_BAR_TITLE, bg=TOPBAR_BACKGROUND)
    t_bar.pack(side="left", expand="yes", fill="both")
    # mechanism = top_moving_mechanism(root, t_bar)
    # t_bar.bind("<B1-Motion>", mechanism.motion_activate)
    tk.Button(f, text="[X]", command=root.destroy).pack(side="right")
    f.pack(side="top", expand="yes", fill="both")
    k.pack(side="top")
    root.mainloop()
    return


# Function Trigger
if __name__ == "__main__":
    main()
