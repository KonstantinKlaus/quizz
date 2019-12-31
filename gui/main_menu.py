import tkinter as tk


class MainMenu(tk.Canvas):

    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)

        self.create_rectangle(790, 100, 1190, 200, fill="blue")
        self.create_rectangle(790, 500, 1190, 400, fill="red")

