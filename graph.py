import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil

class GraphTrends(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller
        self.bg_color = "#1e1e2f"
        self.dot_color = "#00ffcc"
        self.labels = ["CPU Usage", "Memory Usage", "Disk Usage", "Network Sent", "Network Received"]

        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.figure.patch.set_facecolor(self.bg_color)
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors='white')
        self.ax.spines[:].set_color('#888888')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.plot_data()
        self.after(5000, self.update_graph)  # Schedule the update_graph method to be called after 5 seconds

    def stats(self):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        network_sent = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        network_received = net_io.bytes_recv / (1024 * 1024)  # Convert to MB
        return cpu, memory, disk, network_sent, network_received

    def plot_data(self):
        cpu, memory, disk, network_sent, network_received = self.stats()
        data = [cpu, memory, disk, network_sent, network_received]

        self.ax.clear()
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors='green')
        self.ax.spines[:].set_color('#888888')

        for i in range(len(data)):
            self.ax.plot([i], [data[i]], 'o', color=self.dot_color)
            self.ax.annotate(f"{self.labels[i]}: {data[i]:.2f}", (i, data[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='white')

        self.ax.set_xticks(range(len(self.labels)))
        self.ax.set_xticklabels(self.labels, color='white')
        self.ax.set_ylim(0, 100)
        self.ax.set_title("System Performance Trends", color='white')

        self.canvas.draw()

    def update_graph(self):
        self.plot_data()
        self.after(5000, self.update_graph)  # Schedule the next update