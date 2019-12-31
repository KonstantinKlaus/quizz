import logging
import tkinter as tk

from gui.main_menu import MainMenu


class Gui:

    logger = logging.getLogger("log")

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Quiz")

        self.root.attributes('-zoomed', True)

        self.actual_frame = MainMenu(self.root)
        self.actual_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_gui)

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

    def end_gui(self, event=None):
        self.root.destroy()
