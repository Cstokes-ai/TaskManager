import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SchedulingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2E2E2E')
        self.controller = controller
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        tk.Label(self, text="Scheduling Page", font=("Arial", 16, "bold"),
                 fg="white", bg="#2E2E2E").pack(pady=10)

        columns = ("PID", "Name", "Status", "Priority", "CPU", "Context Switches")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e1e2f", foreground="white",
                        fieldbackground="#1e1e2f", rowheight=25)
        style.map("Treeview", background=[('selected', '#3366cc')])

        self.tree.bind("<Double-1>", self.on_process_click)

        self.queue_label = tk.Label(self, text="[Process Queue View ]",
                                    font=("Consolas", 12), fg="white", bg="navy")
        self.queue_label.pack(pady=10)
        tk.Button(self, text="Return to Homepage", command=lambda: self.controller.show_frame("HomePage"),
                    bg="#007BFF", fg="white", font=("Consolas", 12, "bold")).pack(pady=10)
    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for proc in psutil.process_iter(['pid', 'name', 'status', 'nice', 'num_ctx_switches']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                status = proc.info['status']
                nice = proc.info['nice']
                cpu = proc.cpu_num if hasattr(proc, 'cpu_num') else (
                    proc.cpu_affinity()[0] if proc.cpu_affinity() else "N/A")
                ctx = proc.info['num_ctx_switches']
                ctx_str = f"Vol: {ctx.voluntary}, Invol: {ctx.involuntary}" if ctx else "N/A"

                self.tree.insert('', 'end', values=(pid, name, status, nice, cpu, ctx_str))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.after(10000, self.update_table)  # 10 seconds

    def on_process_click(self, event):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "No process selected.")
            return

        values = self.tree.item(selected, 'values')
        pid = int(values[0])
        try:
            proc = psutil.Process(pid)
            self.show_process_window(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            messagebox.showerror("Error", "Unable to access process info.")

    def show_process_window(self, proc):
        popup = tk.Toplevel(self)
        popup.configure(bg="#0A1B3D")
        popup.title(f"Process {proc.pid} Info")
        popup.geometry("600x600")

        def section_title(text):
            return tk.Label(popup, text=text, font=("Arial", 14, "bold"),
                            fg="white", bg="#0A1B3D", pady=10)

        section_title("General Info").pack()
        tk.Label(popup, text=f"Name: {proc.name()}", fg="white", bg="#0A1B3D",
                 font=("Arial", 12)).pack()
        tk.Label(popup, text=f"Status: {proc.status()}", fg="white", bg="#0A1B3D",
                 font=("Arial", 12)).pack()
        tk.Label(popup, text=f"Nice (Priority): {proc.nice()}", fg="white", bg="#0A1B3D",
                 font=("Arial", 12)).pack()

        section_title("CPU Usage").pack()
        tk.Label(popup, text=f"CPU %: {proc.cpu_percent(interval=0.1)}%",
                 fg="white", bg="#0A1B3D", font=("Arial", 12)).pack()

        section_title("Memory Info").pack()
        mem = proc.memory_info()
        tk.Label(popup, text=f"RSS: {mem.rss / (1024 * 1024):.2f} MB",
                 fg="white", bg="#0A1B3D", font=("Arial", 12)).pack()
        tk.Label(popup, text=f"VMS: {mem.vms / (1024 * 1024):.2f} MB",
                 fg="white", bg="#0A1B3D", font=("Arial", 12)).pack()

        section_title("Context Switches").pack()
        ctx = proc.num_ctx_switches()
        tk.Label(popup, text=f"Voluntary: {ctx.voluntary}", fg="white", bg="#0A1B3D",
                 font=("Arial", 12)).pack()
        tk.Label(popup, text=f"Involuntary: {ctx.involuntary}", fg="white", bg="#0A1B3D",
                 font=("Arial", 12)).pack()

        section_title("Scheduling Algorithms Overview").pack()
        scheduler_desc = (
            "Scheduling Algorithms:\n"
            "- First-Come First-Serve (FCFS)\n"
            "- Shortest Job Next (SJN)\n"
            "- Round Robin (RR)\n"
            "- Priority Scheduling\n"
            "- Multi-level Feedback Queue (MLFQ)\n\n"
            "Scheduler Components:\n"
            "- Dispatcher\n"
            "- Ready Queue\n"
            "- I/O Queue\n"
            "- Context Switcher\n"
        )
        tk.Label(popup, text=scheduler_desc, fg="white", bg="#0A1B3D",
                 font=("Consolas", 11), justify="left", wraplength=550).pack(pady=10)

