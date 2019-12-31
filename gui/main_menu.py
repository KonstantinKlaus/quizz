import tkinter as tk

class MainMenu(tk.Frame):

    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)

        self.label = tk.Label(self, text="Hello, World!")
        self.label.pack(padx=20, pady=20)
