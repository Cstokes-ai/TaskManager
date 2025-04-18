import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psutil
import threading
import time

class SchedulingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='navy')
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        title = tk.Label(self, text="Live Scheduling Snapshot", font=("Arial", 20, "bold"), fg="white", bg="navy")
        title.pack(pady=10)

        columns = ("PID", "Name", "Status", "Priority", "CPU Core", "Context Switches")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e1e2f", foreground="white", fieldbackground="#1e1e2f", rowheight=25)
        style.map("Treeview", background=[('selected', '#3366cc')])

        button_frame = tk.Frame(self, bg='navy')
        button_frame.pack(pady=10)

        modify_btn = tk.Button(button_frame, text="Change Priority (Nice)", command=self.change_priority, font=("Arial", 12))
        modify_btn.pack(padx=10, side=tk.LEFT)

        self.queue_label = tk.Label(self, text="[Process Queue View Placeholder]", font=("Arial", 12), fg="white", bg="navy")
        self.queue_label.pack(pady=10)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for proc in psutil.process_iter(['pid', 'name', 'status', 'nice', 'cpu_num', 'num_ctx_switches']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                status = proc.info['status']
                nice = proc.info['nice']
                cpu = proc.info['cpu_num']
                ctx = proc.info['num_ctx_switches']
                ctx_str = f"Vol: {ctx.voluntary}, Invol: {ctx.involuntary}" if ctx else "N/A"

                self.tree.insert('', 'end', values=(pid, name, status, nice, cpu, ctx_str))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.after(3000, self.update_table)  # Update every 3 seconds

    def change_priority(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "No process selected.")
                return

            values = self.tree.item(selected, 'values')
            pid = int(values[0])
            current_priority = int(values[3])
            new_priority = simpledialog.askinteger("Change Priority", f"Enter new nice value for PID {pid} (current: {current_priority}):")

            if new_priority is not None:
                proc = psutil.Process(pid)
                proc.nice(new_priority)
                messagebox.showinfo("Success", f"Priority updated to {new_priority} for PID {pid}.")
        except psutil.AccessDenied:
            messagebox.showerror("Access Denied", "You need to run the app as administrator to change priorities.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
