import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        sidebar = tk.Frame(self, width=150, bg="gray")
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="Home", command=lambda: self.controller.show_frame("HomePage"), width=20).pack(pady=5)
        tk.Button(sidebar, text="CPU", command=lambda: self.controller.show_frame("CPUPage"), width=20).pack(pady=5)
        tk.Button(sidebar, text="Memory", command=lambda: self.controller.show_frame("Memory"), width=20).pack(pady=5)
        tk.Button(sidebar, text="Process", command=lambda: self.controller.show_frame("Process"), width=20).pack(pady=5)
        tk.Button(sidebar, text="Scheduling", command=lambda: self.controller.show_frame("Scheduling"), width=20).pack(pady=5)

        # Logout Button
        tk.Button(sidebar, text="Logout", command=self.logout, width=20).pack(pady=5)

        # Main content area
        content = tk.Frame(self)
        content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(content, text="Real-Time Task Manager", font=("Arial", 16, "bold")).pack()
        tk.Label(content, text="Monitor system performance efficiently and in real time.").pack()

        # Overview Metrics
        self.cpu_usage = tk.StringVar()
        self.memory_usage = tk.StringVar()
        self.process_count = tk.StringVar()

        tk.Label(content, textvariable=self.cpu_usage, font=("Arial", 12)).pack()
        tk.Label(content, textvariable=self.memory_usage, font=("Arial", 12)).pack()
        tk.Label(content, textvariable=self.process_count, font=("Arial", 12)).pack()

        # Footer
        footer = tk.Label(content, text="Version: 1.0 - Beta | Developed with Python, Psutil & Tkinter", font=("Arial", 8))
        footer.pack(side="bottom", pady=10)

    def logout(self):
        self.controller.quit()