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
        title_label = ttk.Label(self, text="CPU & Memory Usage", font=("Arial", 18, "bold"), foreground="green")
        title_label.pack(pady=10)

        # Return to Homepage Button (Top Right)
        back_button = ttk.Button(self, text="Return to Homepage", command=lambda: self.controller.show_frame("HomePage"))
        back_button.place(relx=0.95, rely=0.02, anchor="ne", width=150, height=30)

        # Frame for Stats
        stats_frame = ttk.Frame(self)
        stats_frame.pack(pady=10, padx=10, fill=tk.X)

        # CPU and Memory Stats
        self.cpu_usage = tk.StringVar()
        self.memory_usage = tk.StringVar()
        self.cpu_load = tk.StringVar()
        self.cpu_per_core = [tk.StringVar() for _ in range(psutil.cpu_count())]
        self.memory_used = tk.StringVar()
        self.memory_free = tk.StringVar()
        self.memory_cached = tk.StringVar()

        # CPU and Memory Stats Labels
        ttk.Label(stats_frame, textvariable=self.cpu_usage, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        ttk.Label(stats_frame, textvariable=self.cpu_load, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        for i, var in enumerate(self.cpu_per_core):
            ttk.Label(stats_frame, textvariable=var, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        ttk.Label(stats_frame, textvariable=self.memory_usage, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        ttk.Label(stats_frame, textvariable=self.memory_used, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        ttk.Label(stats_frame, textvariable=self.memory_free, font=("Arial", 12), background="darkslategray", foreground="white").pack()
        ttk.Label(stats_frame, textvariable=self.memory_cached, font=("Arial", 12), background="darkslategray", foreground="white").pack()

        # Graph Frame
        graph_frame = ttk.Frame(self)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Matplotlib Figures for CPU and Memory
        self.fig_cpu, self.ax_cpu = plt.subplots()
        self.fig_mem, self.ax_mem = plt.subplots()

        # Create Canvas for both graphs
        self.canvas_cpu = FigureCanvasTkAgg(self.fig_cpu, master=graph_frame)
        self.canvas_cpu.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_mem = FigureCanvasTkAgg(self.fig_mem, master=graph_frame)
        self.canvas_mem.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

        # Update the CPU Graph
        self.ax_cpu.clear()
        self.ax_cpu.plot(self.cpu_data, label='CPU Usage (%)', color='red')
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.set_title("CPU Usage")
        self.ax_cpu.set_xlabel("Time (s)")
        self.ax_cpu.set_ylabel("Usage (%)")
        self.ax_cpu.legend()

        # Update the Memory Graph
        self.ax_mem.clear()
        self.ax_mem.plot(self.mem_data, label='Memory Usage (%)', color='blue')
        self.ax_mem.set_ylim(0, 100)
        self.ax_mem.set_title("Memory Usage")
        self.ax_mem.set_xlabel("Time (s)")
        self.ax_mem.set_ylabel("Usage (%)")
        self.ax_mem.legend()

        self.canvas_cpu.draw()
        self.canvas_mem.draw()

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
