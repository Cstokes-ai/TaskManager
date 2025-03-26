import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Load the background image using PIL
        image = Image.open(r"C:\Users\corne\OneDrive\Pictures\msi_3d_logo__tech_background_2_by_beman36_dgmknqa-fullview.jpg")
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Add other widgets on top of the background image
        welcome_label = tk.Label(self, text="Welcome to the System Tracker & Task Manager", font=("Arial", 24), bg="white")
        welcome_label.pack(pady=10)

        summary_label = tk.Label(self, text="Quick Summary: \n- CPU Usage: \n- Memory Usage: \n- Running Processes: ", font=("Helvetica", 12), bg="white")
        summary_label.pack(pady=10)