import tkinter as tk
import psutil
import time

class ProcessPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")  # Dark navy background
        self.controller = controller
        self.create_widgets()
        self.process_widgets = {}  # To store process widgets by pid for easy updating
        self.update_process_list()

    def create_widgets(self):
        tech_font = ("Consolas", 12)
        tech_font_bold = ("Consolas", 12, "bold")
        fg_color = "#00ffcc"  # Neon teal
        bg_color = "#1e1e2f"

        # Title
        tk.Label(self, text="Process Manager", font=("Consolas", 18, "bold"),
                 bg=bg_color, fg=fg_color).pack(pady=10)

        # Return Button at the top right
        return_button = tk.Button(self, text="Return to Homepage",
                                  font=tech_font, bg="#333344", fg=fg_color,
                                  activebackground="#444455", activeforeground="#00ffee",
                                  command=lambda: self.controller.show_frame("HomePage"))
        return_button.pack(side="top", anchor="ne", padx=10, pady=10)

        #search bar
        search_frame = tk.Frame(self, bg=bg_color)
        search_frame.pack(pady=10)
        search_label = tk.Label(search_frame, text="Search Process:", font=tech_font, bg=bg_color, fg=fg_color).pack(side= "left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=tech_font, bg="#333344", fg=fg_color)
        self.search_entry.pack(side="left", padx=5)
        search_button = tk.Button(search_frame, text="Search", font=tech_font, bg="#333344", fg=fg_color, command = self.update_process_list
                                  )
        # Memory Usage
        self.memory_label = tk.Label(self, font=tech_font, bg=bg_color, fg="#ffffff")
        self.memory_label.pack(pady=5)

        # Process List with Scrollbar
        self.canvas = tk.Canvas(self, bg=bg_color)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        headers = ["Process Number", "PID", "Application Name", "Status", "Runtime", "Action"]
        for i, header in enumerate(headers):
            tk.Label(self.scrollable_frame, text=header, font=tech_font_bold,
                     bg=bg_color, fg=fg_color).grid(row=0, column=i, padx=10, pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Stop All Processes Button
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

        tech_font = ("Consolas", 12)
        bg_color = "#1e1e2f"
        fg_color = "#cccccc"

        # Iterate through the processes
        for i, proc in enumerate(psutil.process_iter(['pid', 'name', 'status', 'create_time']), start=1):
            runtime = time.strftime("%H:%M:%S", time.gmtime(time.time() - proc.info['create_time']))

            # Check if the widget for this process already exists
            if proc.info['pid'] not in self.process_widgets:
                # If not, create new widgets for this process
                process_widgets = {}
                process_widgets['pid_label'] = tk.Label(self.scrollable_frame, text=proc.info['pid'], font=tech_font,
                                                         bg=bg_color, fg=fg_color)
                process_widgets['name_label'] = tk.Label(self.scrollable_frame, text=proc.info['name'], font=tech_font,
                                                          bg=bg_color, fg=fg_color)
                process_widgets['status_label'] = tk.Label(self.scrollable_frame, text=proc.info['status'], font=tech_font,
                                                           bg=bg_color, fg=fg_color)
                process_widgets['runtime_label'] = tk.Label(self.scrollable_frame, text=runtime, font=tech_font,
                                                            bg=bg_color, fg=fg_color)
                process_widgets['end_button'] = tk.Button(self.scrollable_frame, text="End", font=tech_font,
                                                          bg="#ff4444", fg="#ffffff",
                                                          command=lambda pid=proc.info['pid']: self.end_process(pid))

                # Grid the widgets in the appropriate row
                row = i
                process_widgets['pid_label'].grid(row=row, column=1, padx=10, pady=2)
                process_widgets['name_label'].grid(row=row, column=2, padx=10, pady=2)
                process_widgets['status_label'].grid(row=row, column=3, padx=10, pady=2)
                process_widgets['runtime_label'].grid(row=row, column=4, padx=10, pady=2)
                process_widgets['end_button'].grid(row=row, column=5, padx=10, pady=2)

                # Store the widgets by pid for future reference
                self.process_widgets[proc.info['pid']] = process_widgets
            else:
                # Update the existing runtime label
                self.process_widgets[proc.info['pid']]['runtime_label'].config(text=runtime)

        # Schedule next update
        self.after(5000, self.update_process_list)  # Update every 5 seconds

    def end_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
        except psutil.NoSuchProcess:
            pass

    def stop_all_processes(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] not in ["System", "explorer.exe", "python.exe"]:  # Add essential processes here
                try:
                    proc.terminate()
                except psutil.NoSuchProcess:
                    pass
