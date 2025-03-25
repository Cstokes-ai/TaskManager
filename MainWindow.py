import tkinter as tk
from Homepage import HomePage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Tracker & Task Manager")
        self.geometry("800x600")

        # Define title_font attribute
        self.title_font = ("Arial", 24)

        # Initialize HomePage and pack it
        self.home_page = HomePage(self, self)
        self.home_page.pack(fill="both", expand=True)