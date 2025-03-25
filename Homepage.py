import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.background_image=tk.PhotoImage(file = r"C:\Users\corne\OneDrive\Pictures\msi_3d_logo__tech_background_2_by_beman36_dgmknqa-fullview.jpg")
        welcome_label = tk.Label(self, text="Welcome to the System Tracker & Task Manager", font=("Arial", 24))
        welcome_label.pack(pady=10)

        summary_label = tk.Label(self, text="Quick Summary: \n- CPU Usage: \n- Memory Usage: \n- Running Processes: ", font=("Helvetica", 12))
        summary_label.pack(pady=10)
