import logging
import tkinter as tk

from gui.main_menu import MainMenu


class Gui:

    logger = logging.getLogger("log")

    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-zoomed', True)
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def start_gui(self):
        self.root.mainloop()

    def end_gui(self):
        self.root.destroy()
