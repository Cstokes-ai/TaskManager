import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import threading
import time

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2E2E2E')  # Dark gray background
        self.controller = controller
        self.cpu_data = [0] * 60  # Stores last 60 CPU readings
        self.memory_data = [0] * 60  # Stores last 60 Memory readings

        self.create_widgets()
        self.update_graph()

    def create_widgets(self):
        # Sidebar
        sidebar = tk.Frame(self, width=150, bg='#3A3A3A')  # Slightly lighter gray
        sidebar.pack(side="left", fill="y")

        btn_font = ("Consolas", 10, "bold")
        tk.Button(sidebar, text="Home", font=btn_font, command=lambda: self.controller.show_frame("HomePage"),
                  width=20).pack(pady=5)
        tk.Button(sidebar, text="CPU and Memory", font=btn_font, command=lambda: self.controller.show_frame("CPUPage"),
                  width=20).pack(pady=5)  # Renamed button
        tk.Button(sidebar, text="Process", font=btn_font, command=lambda: self.controller.show_frame("Process"),
                  width=20).pack(pady=5)
        tk.Button(sidebar, text="Scheduling", font=btn_font, command=lambda: self.controller.show_frame("Scheduling"),
                  width=20).pack(pady=5)
        tk.Button(sidebar, text="Graph Trends", font=btn_font,
                  command=lambda: self.controller.show_frame("GraphTrends"),
                  width=20).pack(pady=5)


        tk.Button(sidebar, text="Logout", font=btn_font, command=self.logout, width=20).pack(pady=5)

        # Main content area
        content = tk.Frame(self, bg="#2E2E2E")
        content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(content, text="Real-Time Task Manager", font=("Consolas", 16, "bold"), fg="white", bg="#2E2E2E").pack()
        tk.Label(content, text="Monitor system performance efficiently and in real time.", fg="white",
                 bg="#2E2E2E").pack()

        # Graph Preview
        self.fig = Figure(figsize=(3, 4), dpi=100, facecolor="#2E2E2E")
        self.ax = self.fig.add_subplot(111, facecolor="#1E1E1E")
        self.ax.set_xticks([])  # Hide X-axis
        self.ax.set_ylabel("Usage (%)", color="white")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(axis='y', colors='white')
        self.graph_line, = self.ax.plot(self.cpu_data, 'g-', label="CPU Usage")
        self.memory_line, = self.ax.plot(self.memory_data, 'c-', label="Memory Usage")
        self.ax.legend(loc="upper right", fontsize=8, facecolor="#1E1E1E", edgecolor="white")

        canvas = FigureCanvasTkAgg(self.fig, master=content)
        canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        self.canvas = canvas

        # Footer
        tk.Label(content, text="Version: 1.0 - Beta | Developed with Python, Psutil & Tkinter", font=("Consolas", 8),
                 fg="white", bg="#2E2E2E").pack(side="bottom", pady=10)

    def update_graph(self):
        self.cpu_data.pop(0)
        self.cpu_data.append(psutil.cpu_percent())
        self.memory_data.pop(0)
        self.memory_data.append(psutil.virtual_memory().percent)

        self.graph_line.set_ydata(self.cpu_data)
        self.memory_line.set_ydata(self.memory_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        self.after(1000, self.update_graph)

    def logout(self):
        self.controller.quit()