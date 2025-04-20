import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

style.use('ggplot')

class CPUPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#0A1F44')  # Navy Blue Background
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="CPU & Memory Usage", font=("Consolas", 18, "bold"), fg="lime", bg="#0A1F44")
        title_label.pack(pady=10)

        # Return to Homepage Button
        back_button = ttk.Button(self, text="Return to Homepage", command=lambda: self.controller.show_frame("HomePage"))
        back_button.place(relx=0.95, rely=0.02, anchor="ne", width=150, height=30)

        # Metrics Table
        columns = ("Metric", "Value")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, padx=20)

        # Graphs
        graph_frame = tk.Frame(self, bg="#0A1F44")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, (self.ax_cpu, self.ax_mem) = plt.subplots(2, 1, figsize=(8, 4))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Data Storage
        self.cpu_data = []
        self.mem_data = []
        self.max_data_points = 50

        self.update_stats()
        self.update_graph()

    def update_stats(self):
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # CPU Data
        self.tree.insert("", tk.END, values=("Total CPU Usage", f"{psutil.cpu_percent()}%"))

        load_avg = psutil.getloadavg()
        self.tree.insert("", tk.END, values=("CPU Load (1m,5m,15m)", f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"))

        for i, percent in enumerate(psutil.cpu_percent(percpu=True)):
            self.tree.insert("", tk.END, values=(f"Core {i+1} Usage", f"{percent}%"))

        # Memory Data
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024 ** 3)
        used_gb = mem.used / (1024 ** 3)
        available_gb = mem.available / (1024 ** 3)

        self.tree.insert("", tk.END, values=("Total Memory", f"{total_gb:.2f} GB"))
        self.tree.insert("", tk.END, values=("Used Memory", f"{used_gb:.2f} GB"))
        self.tree.insert("", tk.END, values=("Available Memory", f"{available_gb:.2f} GB"))
        self.tree.insert("", tk.END, values=("Memory Usage", f"{mem.percent}%"))

        self.after(1000, self.update_stats)

    def update_graph(self):
        # Update Data
        self.cpu_data.append(psutil.cpu_percent())
        self.mem_data.append(psutil.virtual_memory().percent)

        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data.pop(0)
            self.mem_data.pop(0)

        # CPU Histogram
        self.ax_cpu.clear()
        self.ax_cpu.bar(range(len(self.cpu_data)), self.cpu_data, color='red')
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.set_title("CPU Usage Over Time", fontsize=10)
        self.ax_cpu.set_xlabel("Time (s)")
        self.ax_cpu.set_ylabel("CPU %")

        # Memory Histogram
        self.ax_mem.clear()
        self.ax_mem.bar(range(len(self.mem_data)), self.mem_data, color='blue')
        self.ax_mem.set_ylim(0, 100)
        self.ax_mem.set_title("Memory Usage Over Time", fontsize=10)
        self.ax_mem.set_xlabel("Time (s)")
        self.ax_mem.set_ylabel("Memory %")

        self.canvas.draw()
        self.after(1000, self.update_graph)