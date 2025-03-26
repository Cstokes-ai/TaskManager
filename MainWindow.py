import tkinter as tk
from Homepage import HomePage
from Login import Login

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Tracker & Task Manager")
        self.geometry("800x600")

        # Container to hold all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.show_welcome_screen()

    def show_welcome_screen(self):
        # Clear any existing frames
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

        welcome_frame = tk.Frame(self.container)
        welcome_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(welcome_frame, text="Welcome to the System Tracker & Task Manager", font=("Arial", 24))
        welcome_label.pack(pady=20)

        description_label = tk.Label(welcome_frame, text="This application helps you track system performance and manage tasks.", font=("Helvetica", 14))
        description_label.pack(pady=10)

        login_button = tk.Button(welcome_frame, text="Login", command=lambda: self.show_frame("Login"))
        login_button.pack(pady=20)

        self.frames["Welcome"] = welcome_frame

    def show_frame(self, page_name):
        # Destroy the current frame if it exists
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

        # Create and store a new instance of the requested page
        if page_name == "HomePage":
            frame = HomePage(self.container, self)
        elif page_name == "Login":
            frame = Login(self.container, self)

        self.frames[page_name] = frame
        frame.pack(fill="both", expand=True)
        frame.tkraise()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()