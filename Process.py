import tkinter as tk
import psutil
import time

class ProcessPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")  # Dark navy background
        self.controller = controller
        self.create_widgets()
        self.process_widgets = {}  # To store process widgets by pid
        self.update_process_list()

    def create_widgets(self):
        tech_font = ("Consolas", 12)
        tech_font_bold = ("Consolas", 12, "bold")
        fg_color = "#00ffcc"
        bg_color = "#1e1e2f"

        # Title
        tk.Label(self, text="Process Manager", font=("Consolas", 18, "bold"),
                 bg=bg_color, fg=fg_color).pack(pady=10)

        # Return Button
        return_button = tk.Button(self, text="Return to Homepage",
                                  font=tech_font, bg="#333344", fg=fg_color,
                                  activebackground="#444455", activeforeground="#00ffee",
                                  command=lambda: self.controller.show_frame("HomePage"))
        return_button.pack(side="top", anchor="ne", padx=10, pady=10)

        # Search bar
        search_frame = tk.Frame(self, bg=bg_color)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Search Process:", font=tech_font, bg=bg_color, fg=fg_color).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=tech_font, bg="#333344", fg=fg_color)
        self.search_entry.pack(side="left", padx=5)
        search_button = tk.Button(search_frame, text="Search", font=tech_font, bg="#333344", fg=fg_color,
                                  command=self.search_processes)
        search_button.pack(side="left", padx=5)

        # Memory usage
        self.memory_label = tk.Label(self, font=tech_font, bg=bg_color, fg="#ffffff")
        self.memory_label.pack(pady=5)

        # Process list with scrollbar
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        headers = ["Process Number", "PID", "Application Name", "Status", "Runtime", "Action"]
        for i, header in enumerate(headers):
            tk.Label(self.scrollable_frame, text=header, font=tech_font_bold,
                     bg=bg_color, fg=fg_color).grid(row=0, column=i, padx=10, pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Stop All Button
        stop_all_button = tk.Button(self, text="Stop All Non-Essential Processes",
                                    font=tech_font, bg="#ff4444", fg="#ffffff",
                                    command=self.stop_all_processes)
        stop_all_button.pack(pady=10)

        # Footer
        footer = tk.Label(self, text="Version: 1.0 - Beta | Developed with Python, Psutil & Tkinter",
                          font=("Consolas", 9), bg=bg_color, fg="#777777")
        footer.pack(side="bottom", pady=10)

    def update_process_list(self):
        # Update memory usage
        memory_info = psutil.virtual_memory()
        memory_usage = f"Memory Usage: {memory_info.used / (1024 ** 2):.2f} MB / {memory_info.total / (1024 ** 3):.2f} GB"
        self.memory_label.config(text=memory_usage)

        self.clear_process_widgets()

        for i, proc in enumerate(psutil.process_iter(['pid', 'name', 'status', 'create_time']), start=1):
            try:
                runtime = time.strftime("%H:%M:%S", time.gmtime(time.time() - proc.info['create_time']))
                self.add_process_to_list(i, proc.info['pid'], proc.info['name'], proc.info['status'], runtime)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.after(30000, self.update_process_list)  # Update every 10 seconds

    def clear_process_widgets(self):
        for widgets in self.process_widgets.values():
            for widget in widgets.values():
                widget.destroy()
        self.process_widgets.clear()

    def add_process_to_list(self, row, pid, name, status, runtime):
        tech_font = ("Consolas", 12)
        bg_color = "#1e1e2f"
        fg_color = "#cccccc"

        process_widgets = {}
        process_widgets['pid_label'] = tk.Label(self.scrollable_frame, text=pid, font=tech_font, bg=bg_color, fg=fg_color)
        process_widgets['name_label'] = tk.Label(self.scrollable_frame, text=name, font=tech_font, bg=bg_color, fg=fg_color)
        process_widgets['status_label'] = tk.Label(self.scrollable_frame, text=status, font=tech_font, bg=bg_color, fg=fg_color)
        process_widgets['runtime_label'] = tk.Label(self.scrollable_frame, text=runtime, font=tech_font, bg=bg_color, fg=fg_color)
        process_widgets['end_button'] = tk.Button(self.scrollable_frame, text="End", font=tech_font, bg="#ff4444", fg="#ffffff",
                                                  command=lambda pid=pid: self.end_process(pid))

        # Grid
        tk.Label(self.scrollable_frame, text=str(row), font=tech_font, bg=bg_color, fg=fg_color).grid(row=row, column=0, padx=10, pady=2)
        process_widgets['pid_label'].grid(row=row, column=1, padx=10, pady=2)
        process_widgets['name_label'].grid(row=row, column=2, padx=10, pady=2)
        process_widgets['status_label'].grid(row=row, column=3, padx=10, pady=2)
        process_widgets['runtime_label'].grid(row=row, column=4, padx=10, pady=2)
        process_widgets['end_button'].grid(row=row, column=5, padx=10, pady=2)

        self.process_widgets[pid] = process_widgets

    def search_processes(self):
        query = self.search_entry.get().lower()
        self.clear_process_widgets()

        if not query:
            self.update_process_list()
            return

        filtered_processes = [
            proc for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time'])
            if proc.info.get('name', '').lower().startswith(query)
        ]

        for i, proc in enumerate(filtered_processes, start=1):
            try:
                runtime = time.strftime("%H:%M:%S", time.gmtime(time.time() - proc.info['create_time']))
                self.add_process_to_list(i, proc.info['pid'], proc.info['name'], proc.info['status'], runtime)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def end_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
        except psutil.NoSuchProcess:
            pass

    def stop_all_processes(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] not in ["System", "explorer.exe", "python.exe"]:
                try:
                    proc.terminate()
                except psutil.NoSuchProcess:
                    pass
