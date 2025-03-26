import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Load the background image using PIL
        image = Image.open(
            r"C:\Users\corne\OneDrive\Pictures\msi_3d_logo__tech_background_2_by_beman36_dgmknqa-fullview.jpg")
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Username label and entry
        username_label = tk.Label(self, text="Username", bg="white")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password label and entry
        password_label = tk.Label(self, text="Password", bg="white")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(self, text="Login", command=self.check_login)
        login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login_user(username, password):
            messagebox.showinfo("Login Successful", "Welcome!")

            # Clear input fields after login
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            self.controller.show_frame("HomePage")  # Switch to HomePage
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


def login_user(username, password):
    # Connect to the database
    conn = sqlite3.connect('user_management.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        # User exists, validate password
        if user[2] == password:  # Assuming password is the third column
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        conn.close()
        return False
