import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class CPUPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self, text="CPU & Memory Usage", font=("Arial", 16, "bold")).pack(pady=10)

        # Back Button
        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("HomePage"))
        back_button.pack(pady=5)
        back_button.lift()
        # CPU and Memory Stats
        self.cpu_usage = tk.StringVar()
        self.memory_usage = tk.StringVar()
        self.cpu_load = tk.StringVar()
        self.cpu_per_core = [tk.StringVar() for _ in range(psutil.cpu_count())]
        self.memory_used = tk.StringVar()
        self.memory_free = tk.StringVar()
        self.memory_cached = tk.StringVar()

        image = Image.open(
            r"C:\Users\corne\OneDrive\Pictures\msi_3d_logo__tech_background_2_by_beman36_dgmknqa-fullview.jpg")
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Display for CPU and memory stats
        ttk.Label(self, textvariable=self.cpu_usage, font=("Arial", 12)).pack()
        ttk.Label(self, textvariable=self.cpu_load, font=("Arial", 12)).pack()
        for i, var in enumerate(self.cpu_per_core):
            ttk.Label(self, textvariable=var, font=("Arial", 12)).pack()
        ttk.Label(self, textvariable=self.memory_usage, font=("Arial", 12)).pack()
        ttk.Label(self, textvariable=self.memory_used, font=("Arial", 12)).pack()
        ttk.Label(self, textvariable=self.memory_free, font=("Arial", 12)).pack()
        ttk.Label(self, textvariable=self.memory_cached, font=("Arial", 12)).pack()

        # Graph Frame
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Data Storage
        self.cpu_data = []
        self.mem_data = []
        self.max_data_points = 50

        # Start Monitoring
        self.update_stats()
        self.update_graph()

    def update_stats(self):
        # CPU Usage (total)
        self.cpu_usage.set(f"Total CPU Usage: {psutil.cpu_percent()}%")

        # Load averages (1, 5, 15 minutes)
        load_avg = psutil.getloadavg()
        self.cpu_load.set(f"CPU Load (1m, 5m, 15m): {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")

        # Per-core CPU usage
        cpu_percentages = psutil.cpu_percent(percpu=True)
        for i, percentage in enumerate(cpu_percentages):
            self.cpu_per_core[i].set(f"Core {i + 1} Usage: {percentage}%")

        # Memory Usage
        virtual_memory = psutil.virtual_memory()
        self.memory_usage.set(f"Memory Usage: {virtual_memory.percent}%")
        self.memory_used.set(f"Used Memory: {self.bytes_to_human(virtual_memory.used)}")
        self.memory_free.set(f"Free Memory: {self.bytes_to_human(virtual_memory.available)}")
        cached_memory = getattr(virtual_memory, 'cached', 0)
        self.memory_cached.set(f"Cached Memory: {self.bytes_to_human(cached_memory)}")

        self.after(1000, self.update_stats)  # Refresh every second

    def update_graph(self):
        # Append new data
        self.cpu_data.append(psutil.cpu_percent())
        self.mem_data.append(psutil.virtual_memory().percent)

        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data.pop(0)
            self.mem_data.pop(0)

        # Update the graph
        self.ax.clear()
        self.ax.plot(self.cpu_data, label='CPU Usage (%)', color='red')
        self.ax.plot(self.mem_data, label='Memory Usage (%)', color='blue')
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Real-Time CPU & Memory Usage")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Usage (%)")
        self.ax.legend()
        self.canvas.draw()

        self.after(1000, self.update_graph)  # Update every second

    def bytes_to_human(self, byte_count):
        # Converts bytes to a human-readable format (GB, MB, KB, etc.)
        if isinstance(byte_count, str):
            return byte_count
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if byte_count < 1024.0:
                return f"{byte_count:.2f} {unit}"
            byte_count /= 1024.0
        return f"{byte_count:.2f} PB"