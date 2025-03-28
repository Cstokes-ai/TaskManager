import tkinter as tk
from PIL import Image, ImageTk

from CPU import CPUPage
from Homepage import HomePage
from Login import Login

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Tracker & Task Manager")
        self.geometry("800x600")

        # Load the background image using PIL
        image = Image.open(r"C:\Users\corne\OneDrive\Pictures\msi_3d_logo__tech_background_2_by_beman36_dgmknqa-fullview.jpg")
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

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
        welcome_frame.tkraise()

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
        elif page_name == "CPUPage":  # Add this line
            frame = CPUPage(self.container, self)  # Instantiate CPUPage

        self.frames[page_name] = frame
        frame.pack(fill="both", expand=True)
        frame.tkraise()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()