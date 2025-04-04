import tkinter as tk
import time

from CPU import CPUPage
from Homepage import HomePage
from Login import Login
from Process import ProcessPage  # Add this import


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Tracker & Task Manager")
        self.geometry("800x600")

        # Set the background color of the window to navy blue using gradient
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Create gradient background
        self.create_gradient()

        # Container to hold all frames
        self.container = tk.Frame(self, bg="#1a1a2e")  # Set the background of the container to navy blue
        self.container.place(relwidth=1, relheight=1)

        self.frames = {}
        self.show_welcome_screen()

    def create_gradient(self):
        # Creates a gradient from dark blue to lighter blue
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#1a1a2e", outline="")
        for i in range(600):
            color = "#{:02x}{:02x}{:02x}".format(int(26 + i * 0.1), int(26 + i * 0.1),
                                                 int(46 + i * 0.1))  # Soft gradient
            self.canvas.create_line(0, i, 800, i, fill=color)

    def show_welcome_screen(self):
        # Clear any existing frames
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

        welcome_frame = tk.Frame(self.container, bg="#1a1a2e")  # Set the background of the frame to navy blue
        welcome_frame.pack(fill="both", expand=True)

        # App Logo (or placeholder text for now)
        logo_label = tk.Label(welcome_frame, text="System Tracker", font=("Consolas", 36, "bold"), fg="white",
                              bg="#1a1a2e")
        logo_label.pack(pady=20)

        # App Slogan
        slogan_label = tk.Label(welcome_frame, text="Monitor and Manage Your System's Performance",
                                font=("Consolas", 16), fg="white", bg="#1a1a2e")
        slogan_label.pack(pady=10)

        # Feature Overview Section
        feature_label = tk.Label(welcome_frame, text="Features:", font=("Consolas", 18, "bold"), fg="white",
                                 bg="#1a1a2e")
        feature_label.pack(pady=10)

        feature_description = tk.Label(welcome_frame,
                                       text="• Track CPU and Memory Usage\n• Manage Running Processes\n• Real-time System Monitoring",
                                       font=("Consolas", 14), fg="white", bg="#1a1a2e", justify="left")
        feature_description.pack(pady=10)

        # Start animated demo
        self.start_demo(welcome_frame)

        # Login button with Consolas font and a modern, corporate style
        login_button = tk.Button(welcome_frame, text="Login", command=lambda: self.show_frame("Login"),
                                 font=("Consolas", 14, "bold"), fg="white", bg="#007BFF",
                                 relief="flat", padx=20, pady=10)
        login_button.pack(pady=30)

        # Hover effect simulation for the login button (change color when hovered over)
        login_button.bind("<Enter>", lambda e: login_button.config(bg="#0056b3"))
        login_button.bind("<Leave>", lambda e: login_button.config(bg="#007BFF"))

        # Call to action
        call_to_action = tk.Label(welcome_frame, text="Get Started with System Monitoring!",
                                  font=("Consolas", 16, "bold"), fg="white", bg="#1a1a2e")
        call_to_action.pack(pady=20)

        self.frames["Welcome"] = welcome_frame
        welcome_frame.tkraise()

    def start_demo(self, frame):
        # Create a progress bar for animated demo (simulating system monitoring)
        self.progress_label = tk.Label(frame, text="System Monitoring Demo", font=("Consolas", 18), fg="white",
                                       bg="#1a1a2e")
        self.progress_label.pack(pady=20)

        self.progress_bar = tk.Canvas(frame, width=300, height=30, bg="#444444", bd=0, highlightthickness=0)
        self.progress_bar.pack(pady=20)

        # Start the animation (simulate progress bar fill)
        self.animate_progress_bar()

    def animate_progress_bar(self):
        # Create a progress bar animation that fills up (simulating system activity)
        self.progress_fill = self.progress_bar.create_rectangle(0, 0, 0, 30, fill="#007BFF")

        for i in range(301):  # Simulating the progress bar filling up
            self.after(i * 10, self.update_progress_bar, i)

    def update_progress_bar(self, width):
        # Update the width of the progress bar
        self.progress_bar.coords(self.progress_fill, 0, 0, width, 30)

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
        elif page_name == "CPUPage":
            frame = CPUPage(self.container, self)
        elif page_name == "Process":
            frame = ProcessPage(self.container, self)  # Add this line

        self.frames[page_name] = frame
        frame.pack(fill="both", expand=True)
        frame.tkraise()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
