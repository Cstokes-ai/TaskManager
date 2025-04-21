import tkinter as tk
from tkinter import ttk
import psutil
import time
import math

class ProcessPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller
        self.current_page = 0
        self.items_per_page = 25
        self.process_data = []
        self.create_widgets()
        self.update_process_data()

    def create_widgets(self):
        tech_font = ("Consolas", 12)
        fg_color = "#00ffcc"
        bg_color = "#1e1e2f"

        tk.Label(self, text="Process Manager", font=("Consolas", 18, "bold"),
                 bg=bg_color, fg=fg_color).pack(pady=10)

        # Return Button
        tk.Button(self, text="Return to Homepage", font=tech_font,
                  bg="#333344", fg=fg_color, command=lambda: self.controller.show_frame("HomePage")
                 ).pack(side="top", anchor="ne", padx=10, pady=10)

        # Memory label
        self.memory_label = tk.Label(self, font=tech_font, bg=bg_color, fg="#ffffff")
        self.memory_label.pack()

        # Treeview setup
        columns = ("pid", "name", "status", "runtime")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=self.items_per_page)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        # End process button
        tk.Button(self, text="End Selected Process", font=tech_font, bg="#ff4444", fg="#ffffff",
                  command=self.end_selected_process).pack(pady=5)

        # Pagination controls
        pagination_frame = tk.Frame(self, bg=bg_color)
        pagination_frame.pack(pady=5)

        self.prev_button = tk.Button(pagination_frame, text="<< Previous", font=tech_font,
                                     command=self.prev_page)
        self.next_button = tk.Button(pagination_frame, text="Next >>", font=tech_font,
                                     command=self.next_page)
        self.page_label = tk.Label(pagination_frame, text="Page 1", font=tech_font, bg=bg_color, fg=fg_color)

        self.prev_button.pack(side="left", padx=5)
        self.page_label.pack(side="left", padx=10)
        self.next_button.pack(side="left", padx=5)

        # Footer
        tk.Label(self, text="Version: 1.0 - Beta | Developed with Python, Psutil & Tkinter",
                 font=("Consolas", 9), bg=bg_color, fg="#777777").pack(side="bottom", pady=10)

    def update_process_data(self):
        self.process_data = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time']):
            try:
                runtime = time.strftime("%H:%M:%S", time.gmtime(time.time() - proc.info['create_time']))
                self.process_data.append((proc.info['pid'], proc.info['name'], proc.info['status'], runtime))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        mem = psutil.virtual_memory()
        self.memory_label.config(text=f"Memory Usage: {mem.used / (1024**2):.2f} MB / {mem.total / (1024**3):.2f} GB")

        self.show_page(self.current_page)
        self.after(10000, self.update_process_data)  # Refresh every 10 sec

    def show_page(self, page_num):
        self.tree.delete(*self.tree.get_children())
        start = page_num * self.items_per_page
        end = start + self.items_per_page
        for row in self.process_data[start:end]:
            self.tree.insert("", "end", values=row)

        total_pages = math.ceil(len(self.process_data) / self.items_per_page)
        self.page_label.config(text=f"Page {page_num + 1} of {max(1, total_pages)}")

        self.prev_button.config(state="normal" if page_num > 0 else "disabled")
        self.next_button.config(state="normal" if end < len(self.process_data) else "disabled")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.process_data):
            self.current_page += 1
            self.show_page(self.current_page)

    def end_selected_process(self):
        selected = self.tree.selection()
        if not selected:
            return
        pid = int(self.tree.item(selected[0])['values'][0])
        try:
            psutil.Process(pid).kill()
        except psutil.NoSuchProcess:
            pass
