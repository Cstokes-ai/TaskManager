import tkinter as tk
from Homepage import HomePage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Tracker & Task Manager")
        self.geometry("800x600")

        # Define title_font attribute
        self.title_font = ("Arial", 24)

        # Container to hold all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.show_frame("Login")

    def show_frame(self, page_name):
        if page_name not in self.frames:
            if page_name == "HomePage":
                frame = HomePage(self.container, self)
            elif page_name == "Login":
                from Login import Login
                frame = Login(self.container, self)
            self.frames[page_name] = frame
            frame.pack(fill="both", expand=True)
        frame = self.frames[page_name]
        frame.tkraise()